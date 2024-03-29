# See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from odoo.exceptions import ValidationError
import re


class BusinessLine(models.Model):
    _name = "business.line"
    _description = "Business Line"

    name = fields.Char("Name", required=True)
    category_id = fields.Many2one("business.category", "Business Category")
    phone = fields.Char("Phone no", required=True)
    email = fields.Char("Email")
    relation = fields.Many2one("relation.relation", "Relation")
    description = fields.Text("Description")
    employee_id = fields.Many2one("hr.employee", "Employee")
    service_history_line_id = fields.One2many('service.history.line', 'business_id', "Service Line")
    attachment_ids = fields.Many2many('ir.attachment', string='Attachment')

    @api.constrains("phone")
    def _check_phone_digits(self):
        for record in self:
            if record.phone:
                length = len(record.phone)
                if length > 10 :
                    raise ValidationError("Phone number should only have 10 digits.")
                if not record.phone.isdigit():
                    raise ValidationError("Phone number should only contain digits.")

    @api.constrains("email")
    def _check_email(self):
        email_pattern = r"[^@]+@[^@]+\.[^@]+"
        for record in self:
            if record.email and not re.match(email_pattern, record.email):
                raise models.ValidationError("Invalid email format")

class HrEmployee(models.Model):

    _inherit = "hr.employee"

    ipushp_ids = fields.One2many("business.line", "employee_id", "iPushp")



class ServiceLine(models.Model):
    _name = "service.history.line"
    _description = "Service Line"


    def _default_emp(self):
        return self.env.user.employee_id

    emp_id = fields.Many2one("hr.employee", "Employee", default=_default_emp, required=True)
    business_id = fields.Many2one("business.line", "Business")
    descriptions = fields.Text("Description")
    feedback = fields.Text("Feedback")
    rating = fields.Selection([('0', 'Bad'), ('1', 'Very Low'), ('2', 'Low'), ('3', 'Normal'),('4', 'High'),('5', 'Excellent')], string='Priority')
