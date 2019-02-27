# See LICENSE file for full copyright and licensing details.

import datetime
from odoo import api, fields, models
from odoo.tools.translate import _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError


class IrAttachement(models.Model):
    _inherit = "ir.attachment"

    attendees_id = fields.Many2one('list.of.attendees', 'Attendess Ref.')


class CoursesType(models.Model):

    _name = 'course.type'

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)


class Trainingcourses(models.Model):

    _name = 'training.courses'

    @api.constrains('duration')
    def _check_duration(self):
        self.ensure_one()
        if len(str(self.duration)) > 3:
            raise ValidationError(
                _("You can not enter duration more than three digits!"))
        if self.duration <= 0:
            raise ValidationError(_("Duration must be greater than 0!"))

    name = fields.Char(string="Course Name", required=True)
    course_type_id = fields.Many2one("course.type", string="Course Category")
    job_id = fields.Many2one('hr.job', 'Applied Job')
    department = fields.Char(related='job_id.name',
                             string="Department", readonly=True)
    training_location = fields.Char("Training Location")
    duration = fields.Integer('Course Duration', required=True)
    duration_type = fields.Selection(
        [('day', 'Days'), ('week', 'Weeks'), ('month', 'Months')],
        required=True)
    local_short_description = fields.Text('Course Short Description')


class TrainingClass(models.Model):

    _name = "training.class"
    _rec_name = "course_id"

    @api.constrains('training_start_date', 'training_end_date')
    def _check_training_dup(self):
        self.ensure_one()
        if self.training_start_date > fields.Date.context_today(self):
            raise ValidationError(_("You can't create past training!"))
        if self.training_start_date > self.training_end_date:
            raise ValidationError(
                _("End Date should be greated than Start date of Training!"))

    course_id = fields.Many2one(
        "training.courses", string="Course Name", required=True)
    department = fields.Char(
        related='course_id.department', string="Department", readonly=True)
    job_id = fields.Many2one(related='course_id.job_id',
                             comodel='hr.job', string='Applied Job',
                             readonly=True)
    course_categ_id = fields.Many2one(
        related='course_id.course_type_id', comodel="course.type",
        string="Course Type", readonly=True)
    training_location = fields.Char(
        related='course_id.training_location',
        string="Training Location", readonly=True)
    training_attendees = fields.Integer('Training Attendees', required=True)
    training_start_date = fields.Date('Training Start Date', readonly=True,
                                      states={'draft': [('readonly', False)]})
    training_end_date = fields.Date('Training End Date', readonly=True,
                                    states={'draft': [('readonly', False)]})
    attendees_ids = fields.One2many(
        "list.of.attendees", 'class_id', string="List of Local Attendees")
    state = fields.Selection([('draft', 'Draft'),
                              ('to_be_approved', 'To Be Approved'),
                              ('approved', 'Approved'),
                              ('completed', 'Completed'),
                              ('cancel', 'Cancelled')],
                             'State', default='draft')
    description = fields.Text('Description')

    @api.onchange('training_start_date', 'course_id')
    def onchange_start_date(self):
        for rec in self:
            if rec.training_start_date and rec.course_id:
                end_date = False
                training_start_date = rec.training_start_date and \
                    datetime.datetime.strftime(rec.training_start_date, 
                                      DEFAULT_SERVER_DATE_FORMAT)
                if rec.course_id.duration and \
                        rec.course_id.duration_type == 'day':
                    end_date = \
                        datetime.datetime.strptime(
                            training_start_date,
                            DEFAULT_SERVER_DATE_FORMAT) + datetime.timedelta(
                            days=rec.course_id.duration - 1)
                elif rec.course_id.duration and \
                        rec.course_id.duration_type == 'week':
                    end_date = datetime.datetime.strptime(
                        training_start_date,
                        DEFAULT_SERVER_DATE_FORMAT) + relativedelta(
                        weeks=rec.course_id.duration, days=-1)
                elif rec.course_id.duration and \
                        rec.course_id.duration_type == 'month':
                    end_date = datetime.datetime.strptime(
                        training_start_date,
                        DEFAULT_SERVER_DATE_FORMAT) + relativedelta(
                        months=rec.course_id.duration, days=-1)
                end_date = end_date and \
                    datetime.datetime.strftime(end_date, 
                                      DEFAULT_SERVER_DATE_FORMAT)                        
                rec.training_end_date = end_date

    @api.multi
    def action_to_be_approve(self):
        self.write({'state': 'to_be_approved'})
        return True

    @api.multi
    def action_approve(self):
        for rec in self:
            if not rec.training_attendees:
                raise ValidationError(
                    _("Training Attendees should not be Zero!"))
            rec.write({'state': 'approved'})
        return True

    @api.multi
    def action_completed(self):
        for rec in self:
            if not rec.attendees_ids:
                raise ValidationError(
                    _("You can not Approve this training which \
                        don't have any attendees!"))
            else:
                if len(rec.attendees_ids.ids) > rec.training_attendees:
                    raise ValidationError(
                        _("List of attendees are greater than \
                            Training Attendees!"))
                for attendee in rec.attendees_ids:
                    if attendee.state not in ('train_completed',
                                              'in_complete'):
                        raise ValidationError(
                            _("You can not Mark the training as Completed \
                                till any of attendee is not in \
                                Training Completed or Training incomplete!"))
            rec.write({'state': 'completed'})
        return True

    @api.multi
    def action_cancel(self):
        for rec in self:
            for attendee in rec.attendees_ids:
                if attendee.state not in ['draft', 'awaiting_training_start',
                                          'in_complete']:
                    raise ValidationError(
                        _("You can not cancel the Training Class if \
                            all attendees are not in Draft, Awaiting \
                            Training Start or In complete state!"))
        self.write({'state': 'cancel'})
        return True


class ListOfAttendees(models.Model):

    _name = "list.of.attendees"
    _rec_name = "class_id"

    @api.constrains('class_id', 'training_start_date', 'training_end_date',
                    'date_of_arrival')
    def _check_training_dup(self):
        self.ensure_one()
        if self.training_start_date < datetime.datetime.now().strftime(
                DEFAULT_SERVER_DATE_FORMAT):
            raise ValidationError(_("You can't create past training!"))
        if self.training_start_date > self.training_end_date:
            raise ValidationError(
                _("End Date should be greater than Start date of Training!"))
        if self.date_of_arrival and \
                self.date_of_arrival < self.training_start_date:
            raise ValidationError(
                _("Arrival Date should be less or equal than \
                    Start date of Training!"))

    _sql_constraints = [
        ('employee_class_unique', 'unique(class_id, employee_id)',
         'You can not add employee multiple times in a Training!'),
    ]

    class_id = fields.Many2one("training.class", string="Training Class")
    employee_id = fields.Many2one("hr.employee", "Employee", readonly=True,
                                  states={
                                      'draft': [('readonly', False)]})
    attendees_image = fields.Binary(
        related="employee_id.image", string="Image")
    training_start_date = fields.Date('Training Start Date', required=True,
                                      readonly=True, states={
                                          'draft': [('readonly', False)]})
    training_end_date = fields.Date('Training End Date', required=True,
                                    readonly=True, states={
                                        'draft': [('readonly', False)]})
    date_of_arrival = fields.Date('Date of Arrival in Training Location',
                                  readonly=True, states={
                                      'draft': [('readonly', False)],
                                      'awaiting_training_start': [('readonly',
                                                                   False)]})
    comments = fields.Text('Comments')
    attachment_ids = fields.One2many(
        'ir.attachment', 'attendees_id', string='Attachments')
    state = fields.Selection([('draft', 'Draft'), ('awaiting_training_start',
                                                   'Awaiting Training Start'),
                              ('in_training', 'In Training'),
                              ('train_completed', 'Training Completed'),
                              ('in_complete', 'Training Incomplete')],
                             string='State', default='draft')

    @api.onchange('class_id')
    def onchange_start_date(self):
        for rec in self:
            if rec.class_id:
                rec.training_start_date = self.class_id.training_start_date
                rec.training_end_date = self.class_id.training_end_date

    @api.multi
    def action_awaiting_training_start(self):
        self.write({'state': 'awaiting_training_start'})
        return True

    @api.multi
    def action_in_training(self):
        for rec in self:
            if not rec.date_of_arrival:
                raise ValidationError(_("Please add Date of arrival!"))
            rec.write({'state': 'train_completed'})
        return True

    @api.multi
    def action_training_completed(self):
        self.write({'state': 'train_completed'})
        return True

    @api.multi
    def action_in_complete(self):
        self.write({'state': 'in_complete'})
        return True

    @api.multi
    def action_cancel(self):
        self.write({'state': 'in_complete'})
        return True
