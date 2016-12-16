# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import models, fields


class res_request(models.Model):
    _name = 'res.request'
    _order = 'date desc'
    _description = 'Request'

    name = fields.Char('Subject', required=True)
    date = fields.Datetime('Date')
    act_from = fields.Many2one('res.users', 'From')
    act_to = fields.Many2one('res.users', 'To')
    body = fields.Text('Request')
