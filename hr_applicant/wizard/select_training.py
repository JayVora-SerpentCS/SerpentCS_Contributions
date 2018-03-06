# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
import datetime
from dateutil.relativedelta import relativedelta


class SelectTraining(models.TransientModel):

    _name = 'select.training'

    is_triaing_needed = fields.Boolean(
        string="Is Training needed?", required=True)

    @api.multi
    def action_done(self):
        applicant = self.env['hr.applicant'].search(
            [('id', '=', self._context.get('active_id'))])
        employee_dict = applicant.create_employee_from_applicant()
        course_obj = self.env['training.courses']
        class_obj = self.env['training.class']
        attendee_obj = self.env['list.of.attendees']
        for rec in self:
            if rec.is_triaing_needed:
                course = course_obj.search(
                    [('job_id', '=', applicant.job_id.id)])
                if not course:
                    course = course_obj.create({
                        'name': 'Training Course for ' + str(
                            applicant.job_id.name),
                        'job_id': applicant.job_id.id,
                        'duration': 1,
                        'duration_type': 'month'})
                training_class = class_obj.search(
                    [('course_id', '=', course.id)])
                if not training_class:
                    training_class = class_obj.create({
                        'course_id': course.id,
                        'training_attendees': 1,
                        'training_start_date': datetime.date.today() +
                        datetime.timedelta(days=1),
                        'training_end_date': datetime.date.today() +
                        datetime.timedelta(days=1) + relativedelta(
                            months=1, days=-1),
                        'state': 'approved'})
                attendee_obj.create({
                    'class_id': training_class.id,
                    'employee_id': employee_dict.get('res_id', False),
                    'training_start_date': training_class.training_start_date,
                    'training_end_date': training_class.training_end_date,
                    'date_of_arrival': training_class.training_start_date,
                    'state': 'in_training'})
        return True
