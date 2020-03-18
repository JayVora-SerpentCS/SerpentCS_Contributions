# -*- coding: utf-8 -*-
# © 2016 Serpent Consulting Services Pvt. Ltd. <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    #Add an option to add the price on the report
    hide_price = fields.Boolean(title='Hide Price',
                                help="If checked, you can hide"
                                     " the price in report of"
                                     " Sales Order.")
