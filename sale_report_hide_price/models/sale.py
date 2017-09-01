# -*- coding: utf-8 -*-
# © 2016 Serpent Consulting Services Pvt. Ltd. <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class sale_order(models.Model):
    _inherit = 'sale.order'

    show_price = fields.Boolean('Show Price', help="If checked, you can see"
                                " the price in report of Sales"
                                " Order / Quotation.")
    show_discount = fields.Boolean('Show Discount', help="""If checked, you
                                    can see the discount in report of"
                                    Sales Order / quotation.""")
