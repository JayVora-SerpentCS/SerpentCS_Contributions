# See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from odoo.exceptions import UserError
import requests, base64


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
    product_variant_id = fields.Many2many('product.product', string='Product Variant(s)',
                                         copy=False)


    @api.onchange('image_url')
    def onchange_image_url(self):
        if self.image_url:
            try:
                data = requests.get(self.image_url)
                if data.status_code == 200:
                    self.image = base64.b64encode(data.content)
                else:
                    raise UserError("Please enter a valid URL.")
            except Exception as e:
                raise UserError(e)


    @api.model
    def create(self, vals):
        if not vals.get('product_multi_variant_id'):
            records = self.env['product.product'].search([('product_tmpl_id', '=', vals['product_tmpl_id'])])
            vals.update({'product_variant_id': [[6, 0, [x.id for x in records]]]})
        return super(ProductImage, self).create(vals)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    images_variant = fields.Many2one('product.image', string='Images')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    images = fields.One2many('product.image', 'product_tmpl_id', 'Images')
    variant_bool = fields.Boolean(string='Show Variant Wise Images',
                                  help='Check if you like to show variant wise'
                                       ' images in WebSite', auto_join=True, default=True)
