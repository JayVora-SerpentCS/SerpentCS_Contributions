# See LICENSE file for full copyright and licensing details.

from datetime import datetime
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Employee(models.Model):
    _inherit = "hr.employee"

    @api.depends("medical_ids")
    def _compute_no_of_medical(self):
        for rec in self:
            rec.no_of_medical = len(rec.medical_ids.ids)

    @api.depends("prev_occu_ids")
    def _compute_no_of_prev_occu(self):
        for rec in self:
            rec.no_of_prev_occu = len(rec.prev_occu_ids.ids)

    @api.depends("relative_ids")
    def _compute_no_of_relative(self):
        for rec in self:
            rec.no_of_relative = len(rec.relative_ids.ids)

    @api.depends("education_ids")
    def _compute_no_of_education(self):
        for rec in self:
            rec.no_of_education = len(rec.education_ids.ids)

    @api.depends("prev_travel_ids")
    def _compute_no_of_prev_travel(self):
        for rec in self:
            rec.no_of_prev_travel = len(rec.prev_travel_ids.ids)

    @api.depends("lang_ids")
    def _compute_no_of_lang(self):
        for rec in self:
            rec.no_of_lang = len(rec.lang_ids.ids)

    medical_ids = fields.One2many(
        "hr.employee.medical.details", "employee_id", "Medical Ref."
    )
    no_of_medical = fields.Integer(
        "No of Medical Detials", compute="_compute_no_of_medical", readonly=True
    )
    prev_occu_ids = fields.One2many(
        "employee.previous.occupation", "employee_id", "Prev. Occupation Ref."
    )
    no_of_prev_occu = fields.Integer(
        "No of Prev. Occupation", compute="_compute_no_of_prev_occu", readonly=True
    )
    relative_ids = fields.One2many("employee.relative", "employee_id", "Relative Ref.")
    no_of_relative = fields.Integer(
        "No of Relative", compute="_compute_no_of_relative", readonly=True
    )
    education_ids = fields.One2many(
        "employee.education", "employee_id", "Education Ref."
    )
    no_of_education = fields.Integer(
        "No of Education", compute="_compute_no_of_education", readonly=True
    )
    prev_travel_ids = fields.One2many(
        "employee.previous.travel", "employee_id", "Previous Travel Ref."
    )
    no_of_prev_travel = fields.Integer(
        "No of Previous Travel", compute="_compute_no_of_prev_travel", readonly=True
    )
    lang_ids = fields.One2many("employee.language", "employee_id", "Language Ref.")
    no_of_lang = fields.Integer(
        "No of Language", compute="_compute_no_of_lang", readonly=True
    )



