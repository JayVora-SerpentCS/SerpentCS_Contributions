# See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SelectTraining(models.TransientModel):
    _name = "select.training"
    _description = "Select Training"

    is_training_needed = fields.Boolean(string="Is Training needed?", required=True)
    applicant_id = fields.Many2one('hr.applicant', "Applicant", store=True)
    job_id = fields.Many2one(related="applicant_id.job_id", store=True)
    training_courses_ids = fields.Many2many("training.class", string="Training")

    # @api.onchange("is_training_needed")
    # def _onchange_training_courses(self):
    #     class_obj = self.env["training.class"]
    #     applicant = self.env["hr.applicant"].browse(self._context.get("active_id"))
    #     for rec in self:
    #         if rec.is_training_needed:
    #             course = class_obj.search([("job_id", "=", applicant.job_id.id)])
    #             domain1 = [("job_id", "=", applicant.job_id.id)]
    #             if not course:
    #                 raise ValidationError(
    #                     _("No course available for this job position")
    #                 )
    #             return {
    #                 "domain": {
    #                     "training_courses_ids": domain1
    #                 }
    #             } 

    def action_done(self):
        applicant = self.env["hr.applicant"].browse(self._context.get("active_id"))
        employee_dict = applicant.create_employee_from_applicant()
        attendee_obj = self.env["list.of.attendees"]
        for training_class in self.training_courses_ids:
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
