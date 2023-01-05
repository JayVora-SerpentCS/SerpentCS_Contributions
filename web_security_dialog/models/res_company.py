# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    security_key = fields.Char('Security Code')

    def check_security(self, vals):
        fields = vals.get('field', False)
        company = self.browse(vals.get('companyId', False)).exists()
        if company and fields and company[fields] and company[fields] == vals.get('password', ''):
            return True
        return False
