# See LICENSE file for full copyright and licensing details.

from datetime import datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class Employee(models.Model):
    _inherit = "hr.employee"

    @api.depends('medical_ids')
    def _compute_no_of_medical(self):
        for rec in self:
            rec.no_of_medical = len(rec.medical_ids.ids)

    @api.depends('prev_occu_ids')
    def _compute_no_of_prev_occu(self):
        for rec in self:
            rec.no_of_prev_occu = len(rec.prev_occu_ids.ids)

    @api.depends('relative_ids')
    def _compute_no_of_relative(self):
        for rec in self:
            rec.no_of_relative = len(rec.relative_ids.ids)

    @api.depends('education_ids')
    def _compute_no_of_education(self):
        for rec in self:
            rec.no_of_education = len(rec.education_ids.ids)

    @api.depends('prev_travel_ids')
    def _compute_no_of_prev_travel(self):
        for rec in self:
            rec.no_of_prev_travel = len(rec.prev_travel_ids.ids)

    @api.depends('lang_ids')
    def _compute_no_of_lang(self):
        for rec in self:
            rec.no_of_lang = len(rec.lang_ids.ids)

    medical_ids = fields.One2many(
        'hr.employee.medical.details', 'employee_id', 'Medical Ref.')
    no_of_medical = fields.Integer(
        'No of Medical Detials', compute='_compute_no_of_medical',
        readonly=True)
    prev_occu_ids = fields.One2many(
        'employee.previous.occupation', 'employee_id', 'Prev. Occupation Ref.')
    no_of_prev_occu = fields.Integer(
        'No of Prev. Occupation', compute='_compute_no_of_prev_occu',
        readonly=True)
    relative_ids = fields.One2many(
        'employee.relative', 'employee_id', 'Relative Ref.')
    no_of_relative = fields.Integer(
        'No of Relative', compute='_compute_no_of_relative', readonly=True)
    education_ids = fields.One2many(
        'employee.education', 'employee_id', 'Education Ref.')
    no_of_education = fields.Integer(
        'No of Education', compute='_compute_no_of_education', readonly=True)
    prev_travel_ids = fields.One2many(
        'employee.previous.travel', 'employee_id', 'Previous Travel Ref.')
    no_of_prev_travel = fields.Integer(
        'No of Previous Travel', compute='_compute_no_of_prev_travel',
        readonly=True)
    lang_ids = fields.One2many(
        'employee.language', 'employee_id', 'Language Ref.')
    no_of_lang = fields.Integer(
        'No of Language', compute='_compute_no_of_lang', readonly=True)


class EmployeeMedicalDetails(models.Model):

    _name = "hr.employee.medical.details"
    _description = "Employee Medical Details"
    _rec_name = 'medical_examination'

    medical_examination = fields.Char('Medical Examination')
    vital_sign = fields.Char('Vital sign')
    date = fields.Date(
        'Date', default=fields.Date.context_today, readonly=True)
    doc_comment = fields.Char('Doctor’s Comments')

    head_face_scalp = fields.Selection(
        [('Abnormal', 'Abnormal'), ('Normal', 'Normal')], 'Head, Face, Scalp')
    nose_sinuses = fields.Selection(
        [('Abnormal', 'Abnormal'), ('Normal', 'Normal')], 'Nose/Sinuses')
    mouth_throat = fields.Selection(
        [('Abnormal', 'Abnormal'), ('Normal', 'Normal')], 'Mouth/Throat')
    ears_tms = fields.Selection(
        [('Abnormal', 'Abnormal'), ('Normal', 'Normal')], 'Ears/TMs')
    eyes_pupils_ocular = fields.Selection(
        [('Abnormal', 'Abnormal'), ('Normal', 'Normal')],
        'Eyes/Pupils/Ocular Motility')
    heart_vascular_system = fields.Selection(
        [('Abnormal', 'Abnormal'), ('Normal', 'Normal')],
        'Heart/Vascular System')
    lungs = fields.Selection(
        [('Abnormal', 'Abnormal'), ('Normal', 'Normal')], 'Lungs')
    abdomen_hernia = fields.Selection(
        [('Abnormal', 'Abnormal'), ('Normal', 'Normal')], 'Abdomen/Hernia')
    msk_strengh = fields.Selection(
        [('Abnormal', 'Abnormal'), ('Normal', 'Normal')], 'MSK-Strength')
    neurological = fields.Selection(
        [('Abnormal', 'Abnormal'), ('Normal', 'Normal')],
        'Neurological (Reflexes, Sensation)')
    glasses_needed = fields.Boolean('Glasses Needed?')
    urine_drug_serene = fields.Selection(
        [('Negative', 'Negetive'), ('Positive', 'Positive')],
        'Urine Drug Serene')
    fit_for_full_duty = fields.Boolean('Fully Fit for Duty?')

    good_health = fields.Boolean('Good Health?')
    serious_illness = fields.Boolean('Series Illness or Disease?')
    broken_bones = fields.Boolean('Broken Bones or Surgery?')
    medications = fields.Boolean('Medications at this time?')
    serious_wound = fields.Boolean('Seriously Wounded?')
    allergic = fields.Boolean('Allergic to any medication?')
    epilepsy = fields.Boolean('Epilepsy')
    history_drug_use = fields.Boolean('Any History of drug use?')

    employee_id = fields.Many2one(
        'hr.employee', 'Employee Ref', ondelete='cascade')
    active = fields.Boolean(string='Active', default=True)
    blood_name = fields.Selection(
        [('A', 'A'), ('B', 'B'), ('O', 'O'), ('AB', 'AB')], "Blood Type")
    blood_type = fields.Selection([('+', '+'), ('-', '-')], 'Blood Type')

    @api.model
    def create(self, vals):
        if (self._context.get('active_model') == 'hr.employee' and
                self._context.get('active_id')):
            vals.update({'employee_id': self._context.get('active_id')})
        return super(EmployeeMedicalDetails, self).create(vals)


class EmployeePreviousOccupation(models.Model):

    _name = "employee.previous.occupation"
    _description = "Recruite Previous Occupation"
    _order = 'to_date desc'
    _rec_name = 'position'

    from_date = fields.Date(string='From Date', required=True)
    to_date = fields.Date(string='To Date', required=True)
    position = fields.Char(string='Position', required=True)
    organization = fields.Char(string='Organization')
    ref_name = fields.Char(string='Reference Name')
    ref_position = fields.Char(string='Reference Position')
    ref_phone = fields.Char(string='Reference Phone')
    active = fields.Boolean(string='Active', default=True)
    employee_id = fields.Many2one(
        'hr.employee', 'Employee Ref', ondelete='cascade')
    email = fields.Char('Email')

    @api.model
    def create(self, vals):
        if (self._context.get('active_model') == 'hr.employee' and
                self._context.get('active_id')):
            vals.update({'employee_id': self._context.get('active_id')})
        return super(EmployeePreviousOccupation, self).create(vals)


class EmployeeRelative(models.Model):

    _name = 'employee.relative'
    _description = "Employee Relatives"
    _rec_name = 'name'

    relative_type = fields.Selection([('Aunty', 'Aunty'),
                                      ('Brother', 'Brother'),
                                      ('Daughter', 'Daughter'),
                                      ('Father', 'Father'),
                                      ('Husband', 'Husband'),
                                      ('Mother', 'Mother'),
                                      ('Sister', 'Sister'),
                                      ('Son', 'Son'), ('Uncle', 'Uncle'),
                                      ('Wife', 'Wife'), ('Other', 'Other')],
                                     string='Relative Type', required=True)
    name = fields.Char(string='Name', size=128, required=True)
    birthday = fields.Date(string='Date of Birth')
    place_of_birth = fields.Char(string='Place of Birth', size=128)
    occupation = fields.Char(string='Occupation', size=128)
    gender = fields.Selection(
        [('Male', 'Male'), ('Female', 'Female')], string='Gender',
        required=False)
    active = fields.Boolean(string='Active', default=True)
    employee_id = fields.Many2one(
        'hr.employee', 'Employee Ref', ondelete='cascade')

    @api.onchange('birthday')
    def onchange_birthday(self):
        if self.birthday and datetime.strptime(
                self.birthday, DEFAULT_SERVER_DATE_FORMAT) >= datetime.today():
            warning = {'title': _('User Alert !'), 'message': _(
                'Date of Birth must be less than today!')}
            self.birthday = False
            return {'warning': warning}

    @api.onchange('relative_type')
    def onchange_relative_type(self):
        if self.relative_type:
            if self.relative_type in ('Brother', 'Father', 'Husband', 'Son',
                                      'Uncle'):
                self.gender = 'Male'
            elif self.relative_type in ('Mother', 'Sister', 'Wife', 'Aunty'):
                self.gender = 'Female'
            else:
                self.gender = ''
        if self.employee_id and not self.relative_type:
            warning = {
                'title': _('Warning!'),
                'message': _('Please select Relative Type!'),
            }
            return {'gender': False, 'warning': warning}

    @api.model
    def create(self, vals):
        if (self._context.get('active_model') == 'hr.employee' and
                self._context.get('active_id')):
            vals.update({'employee_id': self._context.get('active_id')})
        return super(EmployeeRelative, self).create(vals)


class EmployeeEducation(models.Model):
    _name = "employee.education"
    _description = "Employee Education"
    _rec_name = "from_date"
    _order = "from_date"

    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    education_rank = fields.Char('Education Rank')
    school_name = fields.Char(string='School Name', size=256)
    grade = fields.Char('Education Field/Major')
    field = fields.Char(string='Major/Field of Education', size=128)
    illiterate = fields.Boolean('Illiterate')
    active = fields.Boolean(string='Active', default=True)
    employee_id = fields.Many2one(
        'hr.employee', 'Employee Ref', ondelete='cascade')
    edu_type = fields.Selection(
        [('Local', 'Local'), ('Abroad', 'Abroad')], 'School Location',
        default="Local")
    country_id = fields.Many2one('res.country', 'Country')
    state_id = fields.Many2one('res.country.state', 'State')
    province = fields.Char("Province")

    @api.onchange('edu_type')
    def onchange_edu_type(self):
        for rec in self:
            if rec.edu_type == 'Local':
                rec.abroad_country_id = False
            else:
                rec.local_province_id = False
                rec.local_district_id = False

    @api.onchange('illiterate')
    def onchange_illiterate(self):
        for rec in self:
            rec.from_date = False
            rec.to_date = False
            rec.education_rank = ''
            rec.school_name = ''
            rec.grade = ''
            rec.field = ''
            rec.edu_type = ''
            rec.country_id = False
            rec.state_id = False
            rec.province = ''

    @api.model
    def create(self, vals):
        if (self._context.get('active_model') == 'hr.employee' and
                self._context.get('active_id')):
            vals.update({'employee_id': self._context.get('active_id')})
        return super(EmployeeEducation, self).create(vals)

    @api.onchange('from_date', 'to_date')
    def onchange_date(self):
        to_date = self.to_date and datetime.strftime(
                self.to_date, DEFAULT_SERVER_DATE_FORMAT)           
        if to_date and datetime.strptime(
                to_date, DEFAULT_SERVER_DATE_FORMAT) >= datetime.today():
            warning = {'title': _('User Alert !'), 'message': _(
                'To date must be less than today!')}
            self.to_date = False
            return {'warning': warning}
        if self.from_date and self.to_date and self.from_date > self.to_date:
            warning = {'title': _('User Alert !'), 'message': _(
                'To Date %s must be greater than From Date %s !') %
                (self.to_date, self.from_date)}
            self.to_date = False
            return {'warning': warning}


class EmployeePreviousTravel(models.Model):
    _name = "employee.previous.travel"
    _description = "Employee Previous Travel"
    _rec_name = "from_date"
    _order = "from_date"

    from_date = fields.Date(string='From Date', required=True)
    to_date = fields.Date(string='To Date', required=True)
    location = fields.Char(string='Location', size=128, required=True)
    reason = fields.Char('Reason', required=True)
    active = fields.Boolean(string='Active', default=True)
    employee_id = fields.Many2one(
        'hr.employee', 'Employee Ref', ondelete='cascade')

    @api.model
    def create(self, vals):
        if (self._context.get('active_model') == 'hr.employee' and
                self._context.get('active_id')):
            vals.update({'employee_id': self._context.get('active_id')})
        return super(EmployeePreviousTravel, self).create(vals)

    @api.onchange('from_date', 'to_date')
    def onchange_date(self):
        if self.to_date and datetime.strptime(
                self.to_date, DEFAULT_SERVER_DATE_FORMAT) >= datetime.today():
            warning = {'title': _('User Alert !'), 'message': _(
                'To date must be less than today !')}
            self.to_date = False
            return {'warning': warning}
        if self.from_date and self.to_date and self.from_date > self.to_date:
            warning = {'title': _('User Alert !'), 'message': _(
                'To Date %s must be greater than From Date %s !') %
                (self.to_date, self.from_date)}
            self.to_date = False
            return {'warning': warning}


class EmployeeLanguage(models.Model):
    _name = "employee.language"
    _description = "Employee Language"
    _rec_name = "language"
    _order = "id desc"

    language = fields.Char('Language', required=True)
    read_lang = fields.Selection(
        [('Excellent', 'Excellent'), ('Good', 'Good'), ('Poor', 'Poor')],
        string='Read')
    write_lang = fields.Selection(
        [('Excellent', 'Excellent'), ('Good', 'Good'), ('Poor', 'Poor')],
        string='Write')
    speak_lang = fields.Selection(
        [('Excellent', 'Excellent'), ('Good', 'Good'), ('Poor', 'Poor')],
        string='Speak')
    active = fields.Boolean(string='Active', default=True)
    employee_id = fields.Many2one(
        'hr.employee', 'Employee Ref', ondelete='cascade')
    mother_tongue = fields.Boolean('Mother Tongue')

    @api.constrains('mother_tongue')
    def _check_mother_tongue(self):
        self.ensure_one()
        if self.mother_tongue and self.employee_id:
            language_rec = self.search([
                ('employee_id', '=', self.employee_id.id),
                ('mother_tongue', '=', True), ('id', '!=', self.id)],
                limit=1)
            if language_rec:
                raise ValidationError(_("If you want to set '%s' \
                    as a mother tongue, first you have to uncheck mother \
                    tongue in '%s' language.") % (
                    self.language, language_rec.language))

    @api.model
    def create(self, vals):
        if self._context.get('active_model') == 'hr.employee' and \
                self._context.get('active_id'):
            vals.update({'employee_id': self._context.get('active_id')})
        return super(EmployeeLanguage, self).create(vals)
