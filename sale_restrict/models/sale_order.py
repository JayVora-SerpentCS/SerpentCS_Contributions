# See LICENSE file for full copyright and licensing details.

from odoo import _, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    """Inherited the sale order model."""

    _inherit = "sale.order"

    def action_confirm(self):
        zero_price_products = [
            line.product_id.name for line in self.order_line if line.price_unit <= 0.0
        ]
        is_zero_subtotal = [
            line.product_id.name for line in self.order_line if line.price_subtotal <= 0.0
        ]

        if self.env.user.has_group('sale_restrict.group_sales_restrict_user_validation'):
            if zero_price_products:
                message = "Please specify unit price for the following products:\n" + \
                        "\n".join(zero_price_products)
                raise UserError(message)

            if is_zero_subtotal:
                message = "The following products have a zero subtotal:\n" + \
                        "\n".join(is_zero_subtotal)
                raise UserError(message)

            if self.amount_total <= 0.0:
                raise UserError("The total amount of the sale order cannot be zero.")

        return super(SaleOrder, self).action_confirm()

