# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api


class SecurityDialig(models.Model):

    _inherit = 'res.users'

    security_dialog = fields.Char('Security Code')

    @api.multi
    def check_security(self, vals):
        current_fields = vals.get('field').encode('ascii', 'ignore')
        if(vals.get('userId')):
            user_object = self.browse(vals.get('userId'))
            result = user_object.search_read([
                        ('id', '=', vals.get('userId'))], [current_fields])
            if(result[0].get(current_fields or False) == vals.get('password')
               .encode('ascii', 'ignore')):
                return True
            else:
                return False
        return False

