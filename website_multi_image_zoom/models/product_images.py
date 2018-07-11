# -*- encoding: UTF-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-Today Serpent Consulting Services PVT. LTD.
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

from openerp import api, fields, models, tools


class ProductImage(models.Model):
    _name = 'product.image'
    _description = 'Product Image'

    name = fields.Char(string='Name')
    description = fields.Text(string='Description')
    image_alt = fields.Text(string='Image Label')
    image = fields.Binary(string='Image')
    image_small = fields.Binary(
        string='Small Image', compute='_compute_image_small', store=True,
    )
    image_url = fields.Char(string='Image URL')
    product_tmpl_id = fields.Many2one('product.template', 'Product',
                                      copy=False)
    product_variant_id = fields.Many2one('product.product', 'Product Variant',
                                         copy=False)

    @api.depends('image')
    def _compute_image_small(self):
        for this in self:
            this.image_small = tools.image_resize_image_small(this.image)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    images_variant = fields.One2many('product.image', 'product_variant_id',
                                     'Images')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    images = fields.One2many('product.image', 'product_tmpl_id', 'Images')
    variant_bool = fields.Boolean(string='Show Variant Wise Images',
                                  help='Check if you like to show variant wise'
                                       ' images in WebSite', auto_join=True)
