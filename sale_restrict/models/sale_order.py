# See LICENSE file for full copyright and licensing details.

from odoo import _, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    """Inherited the sale order model."""
    _inherit = "sale.order"
    
    
    def action_confirm(self):
        """Overridden to prevent confirming orders with zero-priced real products or zero subtotal."""
        if self.env.user.has_group('sale_restrict.group_sales_restrict_user_validation'):
            for order in self:
                zero_price_lines = []
                for line in order.order_line:
                    # Skip section or note lines
                    if line.display_type:
                        continue
                    # Validate if price_unit or price_subtotal is 0
                    if line.product_id and (line.price_unit <= 0.0 or line.price_subtotal <= 0.0):
                        zero_price_lines.append(line.product_id.display_name)
                if zero_price_lines:
                    raise UserError(_(
                        "Please specify a Unit Price or Quantity for the following products:\n%s"
                    ) % ("\n".join(zero_price_lines)))
        return super().action_confirm()