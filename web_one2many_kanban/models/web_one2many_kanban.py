# Copyright 2016 Serpent Consulting Services Pvt. Ltd
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import http
from odoo.http import request


class WebFieldData(http.Controller):

    @http.route(['/web/fetch_x2m_data'], type='json', auth='public')
    def get_o2x_data(self, **kwargs):
        o2x_records = kwargs.get('o2x_records')
        o2x_datas = []
        for record in o2x_records:
            o2x_model = record.get('relation', False)
            o2x_ids = record.get('raw_value', False)
            if o2x_model:
                o2x_obj = request.env[o2x_model]
                o2x_datas.append(o2x_obj.search_read([('id', 'in', o2x_ids)]))
        return o2x_datas

