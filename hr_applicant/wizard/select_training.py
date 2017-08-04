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

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
import datetime
from dateutil.relativedelta import relativedelta


class SelectTraining(models.TransientModel):

    _name = 'select.training'

    is_triaing_needed = fields.Boolean(string="Is Training needed?", required=True)

    @api.multi
    def action_done(self):
        applicant = self.env['hr.applicant'].search([('id', '=', self._context.get('active_id'))])
        employee_dict = applicant.create_employee_from_applicant()
        course_obj = self.env['training.courses']
        class_obj = self.env['training.class']
        attendee_obj = self.env['list.of.attendees']
        for rec in self:
            if rec.is_triaing_needed:
                course = course_obj.search([('job_id', '=', applicant.job_id.id)])
                if not course:
                    course = course_obj.create({'name': 'Training Course for ' + str(applicant.job_id.name),
                                                'job_id': applicant.job_id.id,
                                                'duration': 1,
                                                'duration_type': 'month'})
                training_class = class_obj.search([('course_id', '=', course.id)])
                if not training_class:
                    training_class = class_obj.create({'course_id': course.id,
                                                       'training_attendees': 1,
                                                       'training_start_date': datetime.date.today() + datetime.timedelta(days=1),
                                                       'training_end_date': datetime.date.today() + datetime.timedelta(days=1) + relativedelta(months=1, days=-1),
                                                       'state': 'approved'})
                attendee = attendee_obj.create({'class_id': training_class.id,
                                                'employee_id': employee_dict.get('res_id', False),
                                                'training_start_date': training_class.training_start_date,
                                                'training_end_date': training_class.training_end_date,
                                                'date_of_arrival': training_class.training_start_date,
                                                'state': 'in_training'})
        return True
