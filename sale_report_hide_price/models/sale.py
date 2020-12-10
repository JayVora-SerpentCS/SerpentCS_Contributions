# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    show_price = fields.Boolean(
        groups="account.group_account_manager"
        "Show Price",
        help="If checked, you can see the price in "
        "report of"
        "Sales Order / Quotation.",
    )
    show_discount = fields.Boolean(
        groups="account.group_account_manager"
        "Show Discount",
        help="If checked, you can see the discount"
        " in report of Sales Order/Quotation.",
    )
