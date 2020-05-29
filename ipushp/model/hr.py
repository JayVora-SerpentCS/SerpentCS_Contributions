# See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class BusinessLine(models.Model):
    _name = 'business.line'
    _description = 'Business Line'

    name = fields.Char('Name', required='1')
    category_id = fields.Many2one('business.category', 'Business Category')
    phone = fields.Char('Phone no', required='1')
    email = fields.Char('Email')
    relation = fields.Many2one('relation.relation', 'Relation')
    description = fields.Text('Description')
    employee_id = fields.Many2one('hr.employee', 'Employee')


class HrEmployee(models.Model):

    _inherit = 'hr.employee'

    ipushp_ids = fields.One2many('business.line', 'employee_id', 'iPushp')
