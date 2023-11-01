# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class BusinessCategory(models.Model):
    _name = "business.category"
    _description = "Business Category"

    name = fields.Char("Name", required=True)

    @api.model
    def create(self, vals):
        existing_category = self.env['business.category'].search([('name', '=', vals.get('name'))])
        if existing_category:
            raise ValidationError("A Business Category with the same name already exists.")

        return super(BusinessCategory, self).create(vals)


class Relation(models.Model):
    _name = "relation.relation"
    _description = "Employee Relation"

    name = fields.Char("Name")
