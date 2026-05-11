# See LICENSE file for full copyright and licensing details.

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestSalesOrderCreditLimit(TransactionCase):
    def setUp(self):
        super().setUp()
        self.user = self.env.ref("base.user_demo")
        self.SalesOrder = self.env["sale.order"]
        self.product = self.env["product.product"].create(
            {
                "name": "Credit Limit Product",
                "list_price": 100.0,
            }
        )

    def _create_partner(self, **values):
        partner_values = {
            "name": "Test Customer",
            "use_partner_credit_limit": True,
            "credit_limit": 500.0,
            "over_credit": False,
        }
        partner_values.update(values)
        return self.env["res.partner"].create(partner_values)

    def _create_sale_order(self, partner, amount_total):
        return self.SalesOrder.with_user(self.user).create(
            {
                "partner_id": partner.id,
                "partner_invoice_id": partner.id,
                "partner_shipping_id": partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "product_uom_qty": 1,
                            "price_unit": amount_total,
                            "tax_id": False,
                        },
                    )
                ],
            }
        )

    def test_create_sales_order_credit_limit_over_credit_bypass(self):
        """Allow confirmation when the partner is flagged to bypass the limit."""
        partner = self._create_partner(over_credit=True, credit_limit=0.0)
        sales_order = self._create_sale_order(partner, 600.0)

        self.assertEqual(sales_order.state, "draft", "Incorrect order status")
        sales_order.with_user(self.user).action_confirm()
        self.assertEqual(sales_order.state, "sale", "Incorrect order status after confirmation")

    def test_confirm_sales_order_raises_when_credit_limit_exceeded(self):
        """Block confirmation when the current order exceeds the partner limit."""
        partner = self._create_partner(credit_limit=500.0)
        sales_order = self._create_sale_order(partner, 600.0)

        with self.assertRaises(UserError):
            sales_order.with_user(self.user).action_confirm()

        self.assertEqual(sales_order.state, "draft", "Order should remain unconfirmed")

    def test_confirm_sales_order_allows_when_within_credit_limit(self):
        """Allow confirmation while the partner remains within the limit."""
        partner = self._create_partner(credit_limit=500.0)
        sales_order = self._create_sale_order(partner, 400.0)

        sales_order.with_user(self.user).action_confirm()

        self.assertEqual(sales_order.state, "sale", "Incorrect order status after confirmation")
