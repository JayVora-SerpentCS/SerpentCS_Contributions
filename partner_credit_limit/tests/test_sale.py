# See LICENSE file for full copyright and licensing details.

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestSalesOrderCreditLimit(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.company.account_use_credit_limit = True

    def test_create_sales_order_credit_limit(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Test Customer",
                "credit_limit": 100.0,
            }
        )
        product = self.env["product.product"].create({"name": "Product 1", "list_price": 150.0})
        sales_order = self.env["sale.order"].create(
            {
                "partner_id": partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": product.id,
                            "product_uom_qty": 1,
                            "price_unit": 150.0,
                            "name": product.name,
                        },
                    ),
                ],
            }
        )

        with self.assertRaises(UserError):
            sales_order.action_confirm()

        partner.over_credit = True
        sales_order.action_confirm()
        self.assertEqual(sales_order.state, "sale")
