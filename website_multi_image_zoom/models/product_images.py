# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProductImage(models.Model):
    _name = 'product.image'
    _description = 'Product Image'

    name = fields.Char(string='Name')
    description = fields.Text(string='Description')
    image_alt = fields.Text(string='Image Label')
    image = fields.Binary(string='Image')
    image_small = fields.Binary(string='Small Image')
    image_url = fields.Char(string='Image URL')
    product_tmpl_id = fields.Many2one('product.template', 'Product',
                                      copy=False)
    product_variant_id = fields.Many2one('product.product', 'Product Variant',
                                         copy=False)


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
