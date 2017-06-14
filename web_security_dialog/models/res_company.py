# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api


class SecurityDialog(models.Model):

    _inherit = 'res.company'

    pincode = fields.Char('Security Code')

    @api.multi
    def check_security(self, vals):
        current_fields = vals.get('field').encode('ascii', 'ignore')
        company_object = self.browse(vals.get('companyId'))
        result = company_object.search_read([
                        ('id', '=', vals.get('companyId'))], [current_fields])
        if(result[0].get(current_fields or '') == vals.get('password')
           .encode('ascii', 'ignore')):
            return True
        else:
            return False
        return False

