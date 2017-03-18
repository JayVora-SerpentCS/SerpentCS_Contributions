# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class SalesOrderextended(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def get_sale_order_stage_data(self):
        self._cr.execute(
            'select state,count(state) from sale_order group by state')
        sale_order_data = self._cr.fetchall()
        return sale_order_data
