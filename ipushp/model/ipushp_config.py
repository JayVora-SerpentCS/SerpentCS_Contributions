# See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class BusinessCategory(models.Model):
    _name = 'business.category'
    _description = 'Business Category'

    name = fields.Char('Name')


class Relation(models.Model):
    _name = 'relation.relation'
    _description = 'Employee Relation'

    name = fields.Char('Name')
