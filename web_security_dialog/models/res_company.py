# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api


class SecurityDialog(models.Model):

    _inherit = 'res.company'

    security_key = fields.Char('Security Code')

    @api.multi
    def check_security(self, vals):
        print ("vals---->>", vals, type(vals.get('password')))
        fields = vals.get('field').encode('ascii', 'ignore')
        print ("fields====>>", fields)
        fields = fields.decode('utf-8')
        result = self.search_read(
            [('id', '=', vals.get('companyId'))],
            [fields])
        print ("hjgj==", result)
        for record in result:
            print ("field==,", record, record.get(fields))
            if(record and record.get(fields or '') == vals.get('password')):
                return True
            else:
                return False
