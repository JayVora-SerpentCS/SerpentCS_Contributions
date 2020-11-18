# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
import datetime
from odoo.exceptions import ValidationError


class SelectTraining(models.TransientModel):

    _name = "select.training"
    _description = "Select Training"

    is_triaing_needed = fields.Boolean(
        string="Is Training needed?", required=True)

    training_courses_ids = fields.Many2many(
        'training.class', string='Training')

    @api.onchange("is_triaing_needed")
    def onchange_training_courses(self):
        for rec in self:
            class_obj = self.env["training.class"]
            applicant = self.env["hr.applicant"].search(
                [("id", "=", self._context.get("active_id"))])
            if rec.is_triaing_needed:
                course = class_obj.search(
                    [("job_id", "=", applicant.job_id.id)])
                if not course:
                    raise ValidationError(
                        "No course availabale for this job position")
                return {'domain': {'training_courses_ids':
                                   [("job_id", "=", applicant.job_id.id),
                                    ("state", "!=", "completed")]}}

    def action_done(self):

        applicant = self.env["hr.applicant"].search(
            [("id", "=", self._context.get("active_id"))])
        employee_dict = applicant.create_employee_from_applicant()
        attendee_obj = self.env["list.of.attendees"]
        class_obj = self.env["training.class"]
        for rec in self.training_courses_ids:
            training_class = class_obj.search([("id", "=", rec.id)])
            attendee_obj.create(
                {
                    "class_id": training_class.id,
                    "employee_id": employee_dict.get("res_id", False),
                    "training_start_date": training_class.training_start_date,
                    "training_end_date": training_class.training_end_date,
                    "date_of_arrival": training_class.training_start_date,
                    "state": "in_training",
                }
            )

        return True
