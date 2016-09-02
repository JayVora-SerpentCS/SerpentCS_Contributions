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

from openerp import http
from openerp.http import request
from openerp.addons.website_sale.controllers import main


class WebsiteSale(main.website_sale):

    @http.route(['/get_variant_images'], type='json', auth='public',
                methods=['POST'])
    def get_variant_images(self, **post):
        variant_images = request.env['product.image'].sudo().\
            search([('product_variant_id', '=', int(post.get('product_id')))])
        images = [img.id for img in variant_images]
        return {'product_rec': images}
