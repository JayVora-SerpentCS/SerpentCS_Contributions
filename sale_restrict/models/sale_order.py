# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011-Today Serpent Consulting Services Pvt. Ltd.
#    (<http://www.serpentcs.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

from openerp import models,fields,api,_
from openerp.exceptions import Warning


class sale_order(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_button_confirm(self):
        zero_price = [x.product_id.name for x in self.order_line if not x.price_unit]
        if zero_price:
            message= _("Please specify unit price for the following products:") + '\n'
            message += '\n'.join(map(str,zero_price))
            raise Warning(message.rstrip())
        return super(sale_order,self).action_button_confirm()
