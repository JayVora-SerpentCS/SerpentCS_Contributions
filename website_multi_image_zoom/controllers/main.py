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

from openerp import http, SUPERUSER_ID
from openerp.http import request
import openerp.addons.website_sale.controllers.main


class website_sale(openerp.addons.website_sale.controllers.main.website_sale):

    @http.route(['/get_variant_images'], type='json', auth='public',
                methods=['POST'])
    def get_variant_images(self, **post):
        (cr, uid, context, pool) = (request.cr, request.uid,
                                    request.context, request.registry)
        pro_img_obj = pool['product.image']
        variant_images_ids = pro_img_obj.search(cr, uid,
                             [('product_variant_id', '=',
                               int(post.get('product_id')))], context=context)
        pro_img_rec = pro_img_obj.browse(cr, SUPERUSER_ID, variant_images_ids,
                                         context=context)
        imgs = []
        for img in pro_img_rec:
            imgs.append(img.id)
        return {'product_rec': imgs}
