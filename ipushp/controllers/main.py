# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request


class website_ipushp(http.Controller):

    @http.route(['/page/iPushp'], type='http', auth="public", website=True)
    def ipushp(self, **kwargs):
        return request.render('ipushp.iPushp', {
            'category_data': request.env['business.category'
                                         ].sudo().search([]),
            'relation_data': request.env['relation.relation'
                                         ].sudo().search([]),
        })

    @http.route(['/contact_ipushp'], type='http', auth="public", website=True)
    def contact_ipushp(self, **kwargs):
        hr_emp_obj = request.env['hr.employee']
        category_id = kwargs.get('business_categ_id')
        if not isinstance(category_id, int):
            category_id = int(category_id)
        if category_id == -1:
                if kwargs.get('category_name'):
                    vals = {
                        'name': kwargs.get('category_name'),
                    }
                    category_id = request.env['business.category'
                                              ].sudo().create(vals)
                    category_id = category_id.id
        if kwargs.get('user_id'):
            employee = hr_emp_obj.sudo().search([('user_id', '=',
                                                  int(kwargs.get('user_id')))])
            contact_details = {
                'name': kwargs.get('name'),
                'phone': kwargs.get('phone'),
                'email': kwargs.get('email'),
                'description': kwargs.get('description'),
                'relation': kwargs.get('relation_id'),
                'category_id': category_id,
            }
            employee.sudo().write({'ipushp_ids': [(0, 0, contact_details)]})
        return request.render('ipushp.ipushp_thanks', {})
