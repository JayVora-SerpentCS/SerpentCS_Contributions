# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResRequest(models.Model):
    _name = 'res.request'
    _order = 'date desc'
    _description = 'Request'

    name = fields.Char('Subject', required=True)
    date = fields.Datetime()
    act_from = fields.Many2one('res.users', 'From')
    act_to = fields.Many2one('res.users', 'To')
    body = fields.Text(string='Request')
