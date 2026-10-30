# See LICENSE file for full copyright and licensing details.

from odoo import Command, fields
from odoo.exceptions import AccessError, UserError
from odoo.tests import tagged

from odoo.addons.sale.tests.common import TestSaleCommon


@tagged("post_install", "-at_install")
class TestSalesOrderCreditLimit(TestSaleCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.company.account_use_credit_limit = True
        cls.partner_a.credit_limit = 100.0
        cls.product = cls.company_data["product_order_no"]
        cls.foreign_currency = cls.env["res.currency"].create(
            {
                "name": "XCL",
                "symbol": "XCL",
                "rounding": 0.01,
            }
        )
        cls.env["res.currency.rate"].create(
            {
                "name": "2020-01-01",
                "rate": 2.0,
                "currency_id": cls.foreign_currency.id,
                "company_id": cls.env.company.id,
            }
        )
        cls.foreign_pricelist = cls.env["product.pricelist"].create(
            {
                "name": "Credit limit foreign currency",
                "currency_id": cls.foreign_currency.id,
            }
        )

    def _order(self, amount=150.0, **values):
        return self.env["sale.order"].create(
            {
                "partner_id": self.partner_a.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": self.product.id,
                            "product_uom_qty": 1,
                            "price_unit": amount,
                            "tax_ids": [Command.clear()],
                        }
                    )
                ],
                **values,
            }
        )

    def _invoice(self, amount=150.0, **values):
        return self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": self.partner_a.id,
                "invoice_date": fields.Date.today(),
                "invoice_line_ids": [
                    Command.create(
                        {
                            "product_id": self.product.id,
                            "quantity": 1,
                            "price_unit": amount,
                            "tax_ids": [Command.clear()],
                        }
                    )
                ],
                **values,
            }
        )

    def test_order_block_and_override(self):
        order = self._order()
        with self.assertRaisesRegex(UserError, "Allow Over Credit"):
            order.action_confirm()
        self.assertEqual(order.state, "draft")
        self.partner_a.over_credit = True
        order.action_confirm()
        self.assertEqual(order.state, "sale")

    def test_order_at_limit(self):
        order = self._order(100)
        order.action_confirm()
        self.assertEqual(order.state, "sale")

    def test_disabled_company_limit(self):
        self.env.company.account_use_credit_limit = False
        self._order().action_confirm()
        self._invoice().action_post()

    def test_zero_limit_is_unlimited(self):
        self.partner_a.credit_limit = 0
        self._order().action_confirm()
        self._invoice().action_post()

    def test_commercial_partner_override(self):
        child = self.env["res.partner"].create(
            {
                "name": "Credit limit contact",
                "parent_id": self.partner_a.id,
            }
        )
        order = self._order(partner_id=child.id)
        with self.assertRaises(UserError):
            order.action_confirm()
        self.partner_a.over_credit = True
        order.action_confirm()
        self.assertEqual(order.state, "sale")

    def test_foreign_currency_order_below_limit(self):
        order = self._order(150, pricelist_id=self.foreign_pricelist.id)
        self.assertAlmostEqual(order.amount_total / order.currency_rate, 75)
        order.action_confirm()
        self.assertEqual(order.state, "sale")

    def test_foreign_currency_order_above_limit(self):
        order = self._order(250, pricelist_id=self.foreign_pricelist.id)
        with self.assertRaises(UserError):
            order.action_confirm()

    def test_salesperson_without_accounting_access(self):
        user = self.company_data["default_user_salesman"]
        with self.assertRaises(AccessError):
            self.partner_a.with_user(user).read(["credit_limit"])
        order = self._order(50, user_id=user.id).with_user(user)
        order.action_confirm()
        self.assertEqual(order.state, "sale")
        with self.assertRaises(UserError):
            self._order(150, user_id=user.id).with_user(user).action_confirm()

    def test_invoice_block_and_override(self):
        invoice = self._invoice()
        with self.assertRaisesRegex(UserError, "Allow Over Credit"):
            invoice.action_post()
        self.assertEqual(invoice.state, "draft")
        self.partner_a.over_credit = True
        invoice.action_post()
        self.assertEqual(invoice.state, "posted")

    def test_foreign_currency_invoice_below_limit(self):
        invoice = self._invoice(150, currency_id=self.foreign_currency.id)
        self.assertAlmostEqual(invoice.tax_totals["total_amount"], 75)
        invoice.action_post()
        self.assertEqual(invoice.state, "posted")

    def test_foreign_currency_invoice_above_limit(self):
        invoice = self._invoice(250, currency_id=self.foreign_currency.id)
        with self.assertRaises(UserError):
            invoice.action_post()

    def test_sale_invoice_not_counted_twice(self):
        order = self._order(100)
        order.action_confirm()
        invoice = order._create_invoices()
        self.partner_a.invalidate_recordset(["credit", "credit_to_invoice"])
        self.assertAlmostEqual(self.partner_a.credit_to_invoice, 100)
        invoice.action_post()
        self.assertEqual(invoice.state, "posted")
        self.partner_a.invalidate_recordset(["credit", "credit_to_invoice"])
        self.assertAlmostEqual(self.partner_a.credit, 100)
        self.assertAlmostEqual(self.partner_a.credit_to_invoice, 0)

    def test_existing_receivable_blocks_order(self):
        self._invoice(80).action_post()
        with self.assertRaises(UserError):
            self._order(30).action_confirm()

    def test_confirmed_order_blocks_next_order(self):
        self._order(80).action_confirm()
        with self.assertRaises(UserError):
            self._order(30).action_confirm()

    def test_batch_orders_cannot_bypass_limit(self):
        orders = self._order(60) | self._order(60)
        with self.assertRaises(UserError):
            orders.action_confirm()
        self.assertEqual(orders.mapped("state"), ["draft", "draft"])

    def test_batch_invoices_cannot_bypass_limit(self):
        invoices = self._invoice(60) | self._invoice(60)
        with self.assertRaises(UserError):
            invoices.action_post()
        self.assertEqual(invoices.mapped("state"), ["draft", "draft"])

    def test_refund_and_vendor_bill_not_blocked(self):
        for move_type in ("out_refund", "in_invoice"):
            move = self._invoice(move_type=move_type)
            move.action_post()
            self.assertEqual(move.state, "posted")

    def test_order_uses_document_company(self):
        company2 = self.setup_other_company()["company"]
        company2.account_use_credit_limit = True
        self.partner_a.with_company(company2).credit_limit = 20
        self.partner_a.credit_limit = 100
        # Check a company-1 document while company 2 is active in the UI.
        order = self._order(50).with_company(company2)
        order.action_confirm()
        self.assertEqual(order.state, "sale")
