# See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class SecurityDialog(models.Model):

    _inherit = 'res.company'

    security_key = fields.Char('Security Code')

    @api.multi
    def check_security(self, vals):
        fields = vals.get('field').encode('ascii', 'ignore')
        fields = fields.decode('utf-8')
        result = self.search_read(
            [('id', '=', vals.get('companyId'))],
            [fields])
        for record in result:
            if(record and record.get(fields or '') == vals.get('password')):
                return True
            else:
                return False
