# See LICENSE file for full copyright and licensing details.

from odoo.tests.common import TransactionCase


class TestSalesOrderCreditLimit(TransactionCase):
    def test_create_sales_order_credit_limit(self):
        """Test the creation and processing of a sales order"""
        # Create a user and log in as a Sales Manager
        user = self.env.ref("base.user_demo")
        self.env = self.env(user=user)
        SalesOrder = self.env["sale.order"]

        # Create a customer
        partner = self.env["res.partner"].create({"name": "Test Customer", "over_credit": True})

        # Create products
        product1 = self.env["product.product"].create({"name": "Product 1"})
        product2 = self.env["product.product"].create({"name": "Product 2"})

        # Create a sales order
        sales_order = SalesOrder.create(
            {
                "partner_id": partner.id,
                "order_line": [
                    (0, 0, {"product_id": product1.id, "product_uom_qty": 5}),
                    (0, 0, {"product_id": product2.id, "product_uom_qty": 3}),
                ],
            }
        )

        # Check if the sales order is successfully created
        self.assertTrue(sales_order, "Failed to create sales order")

        # Check the order status
        self.assertEqual(sales_order.state, "draft", "Incorrect order status")

        # Confirm the sales order
        sales_order.action_confirm()

        # Check if the order status changes to 'sale'
        self.assertEqual(sales_order.state, "sale", "Incorrect order status after confirmation")
