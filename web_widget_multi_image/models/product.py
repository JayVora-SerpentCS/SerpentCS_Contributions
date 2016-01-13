# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp.osv import osv, fields


class multi_images(osv.osv):
    _name = "multi.images"

    _columns = {
        'image': fields.binary('Images'),
        'description': fields.char('Description'),
        'title': fields.char('title'),
        'product_template_id': fields.many2one('product.template', 'Product')
    }


class product_template(osv.osv):
    _inherit = "product.template"

    _columns = {
        'multi_images': fields.one2many('multi.images', 'product_template_id',
                                        'Multi Images'),
    }
