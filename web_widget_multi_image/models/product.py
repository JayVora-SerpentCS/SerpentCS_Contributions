# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class MultiImages(models.Model):
    _name = "multi.images"

    image = fields.Binary('Images')
    description = fields.Char('Description')
    title = fields.Char('title')
    product_template_id = fields.Many2one('product.template', 'Product')


class ProductTemplate(models.Model):
    _inherit = "product.template"

    multi_images = fields.One2many('multi.images', 'product_template_id',
                                   'Multi Images')
