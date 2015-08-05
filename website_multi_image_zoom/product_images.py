# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011-Till Today Serpent Consulting Services PVT. LTD.
#    (<http://www.serpentcs.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
############################################################################

from openerp import models,fields,api

class product_image(models.Model):
    _name = 'product.image'

    name = fields.Char(string='Name')
    description = fields.Text(string='Description')
    image_alt = fields.Text(string='Image Label')
    image = fields.Binary(string='Image')
    image_small = fields.Binary(string='Small Image')
    image_url = fields.Char(string='Image Url')
    product_tmpl_id = fields.Many2one('product.template','Product')

class product_product(models.Model):
    _inherit = 'product.product'

    images = fields.One2many(related='product_tmpl_id.images',string='Images')

class product_template(models.Model):
    _inherit = 'product.template'

    images = fields.One2many('product.image','product_tmpl_id','Images')
