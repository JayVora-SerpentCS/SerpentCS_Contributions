# -*- coding: utf-8 -*-
##############################################################################
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 Serpent Consulting Services (<http://serpentcs.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from openerp import models, fields, api
import datetime
from dateutil.relativedelta import relativedelta


class SelectTraining(models.TransientModel):

    _name = 'select.training'

    is_triaing_needed = fields.Boolean(string="Is Training needed?",
                                       required=True)

    @api.multi
    def action_done(self):
        act_id = self._context.get('active_id')
        applicant = self.env['hr.applicant'].search([('id', '=', act_id)])
        employee_dict = applicant.create_employee_from_applicant()
        course_obj = self.env['training.courses']
        class_obj = self.env['training.class']
        attendee_obj = self.env['list.of.attendees']
        for rec in self:
            if rec.is_triaing_needed:
                course = course_obj.search([('job_id', '=',
                                             applicant.job_id.id)])
                if not course:
                    t_nam = 'Training Course for ' + str(applicant.job_id.name)
                    course = course_obj.create({'name': t_nam,
                                                'job_id': applicant.job_id.id,
                                                'duration': 1,
                                                'duration_type': 'month'})
                training_class = class_obj.search([('course_id', '=',
                                                    course.id)])
                if not training_class:
                    dt_now = datetime.date.today()
                    tri_class_val = {
                        'course_id': course.id,
                        'training_attendees': 1,
                        'training_start_date': dt_now +
                        datetime.timedelta(days=1),
                        'training_end_date': dt_now +
                        datetime.timedelta(days=1) + relativedelta(months=1,
                                                                   days=-1),
                        'state': 'approved'}
                    training_class = class_obj.create(tri_class_val)
                st_dt = training_class.training_start_date
                attendee_obj.create({
                    'class_id': training_class.id,
                    'employee_id': employee_dict.get('res_id', False),
                    'training_start_date': st_dt,
                    'training_end_date': training_class.training_end_date,
                    'date_of_arrival': st_dt,
                    'state': 'in_training'})
        return True
