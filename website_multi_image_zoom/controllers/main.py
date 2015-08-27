#!/usr/bin/python
# -*- coding: utf-8 -*-
from openerp import http, SUPERUSER_ID
from openerp.http import request
import werkzeug
from openerp.http import request
import openerp.addons.website_sale.controllers.main
from openerp.tools.translate import _
from openerp.addons.website.models.website import slug

class website_sale(openerp.addons.website_sale.controllers.main.website_sale):

    @http.route(['/get_variant_images'], type='json', auth='public', methods=['POST'])
    def get_variant_images(self, **post):
        (cr, uid, context, pool) = (request.cr, request.uid, request.context, request.registry)
        pro_img_obj = pool['product.image']
        variant_images_ids = pro_img_obj.search(cr, uid, [('product_variant_id', '=', int(post.get('product_id')))], context=context)
        pro_img_rec = pro_img_obj.browse(cr, SUPERUSER_ID, variant_images_ids, context=context)
        imgs = []
        for img in pro_img_rec:
            imgs.append(img.id)
        return {'product_rec': imgs}

