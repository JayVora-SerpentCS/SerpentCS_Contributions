from odoo import api, fields, models


class HidePriceDiscount(models.TransientModel):
    """Hide Price Discount Model."""

    _name = 'hide.price.discount'
    _description = "Hide Price Discount Wizard"

    show_price = fields.Boolean(
        'Show Price',
        help="If checked, you can see the price in report of Sales Order / Quotation.")
    show_discount = fields.Boolean(
        'Show Discount',
        help="If checked, you can see the discount in report of Sales Order/Quotation.")

    def hide_price_discount_report(self):
        data = {
            'show_price': self.show_price,
            'show_discount': self.show_discount
        }
        return self.env.ref('sale.action_report_saleorder').report_action([], data=data)
