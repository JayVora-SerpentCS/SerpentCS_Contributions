# -*- coding: utf-8 -*-
# © 2016 Serpent Consulting Services Pvt. Ltd. <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api
from openerp import fields, models

class BillOrder(models.Model):
    _inherit = 'account.invoice'

    #Add an option to add the price on the report
    hide_price = fields.Boolean(title='Hide Price',
                                help="If checked, you can hide"
                                     " the price in report of"
                                     " Sales Order.",
                                compute="_getSaleShowPrice")

    def _getSaleShowPrice(self):
        #When a invoice come from a previous Sale, the field show_price
        #keep the same value. It has to be taken from the DB sale.order

        #Get the name of the previous sale
        tempo = self._get_current_name()

        #If the name is defined, we can search for the the sale_order
        if(tempo):
            saleOrder = self.env['sale.order'].search([('name', '=', tempo)], limit=1)

            #Redefine the value of the field hide_price of this view
            if(saleOrder):
                self.hide_price = saleOrder.hide_price

    @api.one
    def _get_current_name(self):
        #Return the current name of the previous sale
        return self.name
