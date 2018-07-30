# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields


class BusinessLine(models.Model):

    _name = 'business.line'
    _description = 'Business Line'

    name = fields.Char('Name',required=True)
    category_id = fields.Many2one('business.category','Business Category')
    phone = fields.Char('Phone no',required=True)
    email = fields.Char('Email')
    relation = fields.Many2one('relation.relation','Relation')
    description = fields.Text('Description')
    employee_id = fields.Many2one('hr.employee','Employee')
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [('draft','Draft'),
         ('validate', 'Approved'),
         ('cancel', 'Cancelled')],
        string='State',
        default='draft',
    )

    @api.multi
    def action_draft(self):
        return self.write({'state': 'draft'})

    @api.multi
    def action_approve(self):
        return self.write({'state': 'validate'})

    @api.multi
    def action_refuse(self):
        return self.write({'state': 'cancel'})


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    ipushp_ids = fields.One2many('business.line','employee_id','iPushp')
