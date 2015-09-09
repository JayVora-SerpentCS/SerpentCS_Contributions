# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-Today Serpent Consulting Services Pvt. Ltd.
#                            (<http://www.serpentcs.com>)
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

from openerp import models, fields


class sale_order(models.Model):
    _inherit = 'sale.order'

    print_image = fields.Boolean('Print Image', help="""If ticked, you can see
                    the product image in report of sale order/quotation""")
    image_sizes = fields.Selection([('image', 'Big sized Image'),
                                    ('image_medium', 'Medium Sized Image'),
                                    ('image_small', 'Small Sized Image')],
                                   'Image Sizes',
                                   default="image_small",
                                   help="Image size to be displayed in report")


class sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    image_small = fields.Binary('Product Image',
                                related='product_id.image_small')
