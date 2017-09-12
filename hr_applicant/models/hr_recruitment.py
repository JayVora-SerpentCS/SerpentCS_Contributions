# -*- coding: utf-8 -*-
##############################################################################
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 Serpent Consulting Services (<http://serpentcs.com>)
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

from datetime import datetime
from odoo import api, fields, models
from odoo.tools.translate import _
from odoo.exceptions import ValidationError
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF


class Applicant(models.Model):
    _inherit = "hr.applicant"
    _description = "Applicant"

    @api.depends('medical_ids')
    def _compute_no_of_medical(self):
        for rec in self:
            rec.no_of_medical = len(rec.medical_ids.ids)
            rec.no_of_medical1 = len(rec.medical_ids.ids)

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

    medical_ids = fields.One2many('hr.applicant.medical.details',
                                  'applicant_id', 'Medical Ref.')
    no_of_medical = fields.Integer('No of Medical Detials',
                                   compute='_compute_no_of_medical',
                                   readonly=True)
    no_of_medical1 = fields.Integer('No of Medical Detials',
                                    compute='_compute_no_of_medical',
                                    readonly=True)
    prev_occu_ids = fields.One2many('applicant.previous.occupation',
                                    'applicant_id', 'Prev. Occupation Ref.')
    no_of_prev_occu = fields.Integer('No of Prev. Occupation',
                                     compute='_compute_no_of_prev_occu',
                                     readonly=True)
    relative_ids = fields.One2many('applicant.relative', 'applicant_id',
                                   'Relative Ref.')
    no_of_relative = fields.Integer('No of Relative',
                                    compute='_compute_no_of_relative',
                                    readonly=True)
    education_ids = fields.One2many('applicant.education', 'applicant_id',
                                    'Education Ref.')
    no_of_education = fields.Integer('No of Education',
                                     compute='_compute_no_of_education',
                                     readonly=True)
    prev_travel_ids = fields.One2many('applicant.previous.travel',
                                      'applicant_id', 'Previous Travel Ref.')
    no_of_prev_travel = fields.Integer('No of Previous Travel',
                                       compute='_compute_no_of_prev_travel',
                                       readonly=True)
    lang_ids = fields.One2many('applicant.language', 'applicant_id',
                               'Language Ref.')
    no_of_lang = fields.Integer('No of Language',
                                compute='_compute_no_of_lang', readonly=True)

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        ir_actions_report = self.env['ir.actions.report.xml']
        res = super(Applicant, self).fields_view_get(view_id=view_id,
                                                     view_type=view_type,
                                                     toolbar=toolbar,
                                                     submenu=submenu)
        reports = ir_actions_report.search([('report_name', '=',
                                             'hr_applicant.applicant_profile')
                                            ])
        if reports and view_type != 'form':
            new_reports = []
            for rec in res.get('toolbar', {}).get('print', []):
                if rec.get('id', False) not in reports.ids:
                    new_reports.append(rec)
            res.get('toolbar', {})['print'] = new_reports
        return res

    @api.multi
    def create_employee_from_applicant(self):
        res = super(Applicant, self).create_employee_from_applicant()
        applicant_med_obj = self.env['hr.applicant.medical.details']
        emp_med_obj = self.env['hr.employee.medical.details']
        occupation_obj = self.env['applicant.previous.occupation']
        emp_occupation_obj = self.env['employee.previous.occupation']
        attch_obj = self.env['ir.attachment']
        applicant_trav_obj = self.env['applicant.previous.travel']
        emp_trav_obj = self.env['employee.previous.travel']
        if res.get('res_id', False):
            for applicant in self:
                for medical_detail in applicant_med_obj.search(
                        [('applicant_id', '=', applicant.id)]):
                    val = {'medical_examination': medical_detail and
                           medical_detail.medical_examination,
                           'vital_sign': medical_detail.vital_sign,
                           'date': medical_detail.date,
                           'doc_comment': medical_detail.doc_comment,
                           'head_face_scalp': medical_detail and
                           medical_detail.head_face_scalp,
                           'nose_sinuses': medical_detail and
                           medical_detail.nose_sinuses,
                           'mouth_throat': medical_detail and
                           medical_detail.mouth_throat,
                           'ears_tms': medical_detail.ears_tms,
                           'eyes_pupils_ocular': medical_detail and
                           medical_detail.eyes_pupils_ocular,
                           'heart_vascular_system': medical_detail and
                           medical_detail.heart_vascular_system,
                           'lungs': medical_detail.lungs,
                           'abdomen_hernia': medical_detail and
                           medical_detail.abdomen_hernia,
                           'msk_strengh': medical_detail.msk_strengh,
                           'neurological': medical_detail.neurological,
                           'glasses_needed': medical_detail and
                           medical_detail.glasses_needed,
                           'urine_drug_serene': medical_detail and
                           medical_detail.urine_drug_serene,
                           'fit_for_full_duty': medical_detail and
                           medical_detail.fit_for_full_duty,
                           'good_health': medical_detail.good_health,
                           'serious_illness': medical_detail and
                           medical_detail.serious_illness,
                           'broken_bones': medical_detail.broken_bones,
                           'medications:': medical_detail.medications,
                           'serious_wound': medical_detail.serious_wound,
                           'allergic': medical_detail.allergic,
                           'epilepsy': medical_detail.epilepsy,
                           'history_drug_use': medical_detail and
                           medical_detail.history_drug_use,
                           'employee_id': res.get('res_id', False),
                           'blood_name': medical_detail.blood_name,
                           'blood_type': medical_detail.blood_type}
                    medical_id = emp_med_obj.create(val)
                    medical_attach =\
                        attch_obj.search([('res_model', '=',
                                           'hr.applicant.medical.details'),
                                          ('res_id', '=', medical_detail.id)])
                    for medical_attachment in medical_attach:
                        emp_medical_attachment = medical_attachment.copy()
                        emp_medical_attachment.write({
                            'res_model': 'hr.employee.medical.details',
                            'res_id': medical_id.id})
                for prev_occupation in occupation_obj.search([
                        ('applicant_id', '=', applicant.id)]):
                    occupation_id = emp_occupation_obj.create({
                        'from_date': prev_occupation.from_date,
                        'to_date': prev_occupation.to_date,
                        'position': prev_occupation.position,
                        'organization': prev_occupation and
                        prev_occupation.organization,
                        'ref_name': prev_occupation.ref_name,
                        'ref_position': prev_occupation and
                        prev_occupation.ref_position,
                        'ref_phone': prev_occupation.ref_phone,
                        'employee_id': res.get('res_id', False),
                        'email': prev_occupation.email})
                    occupation_attachments = \
                        attch_obj.search([('res_model', '=',
                                           'applicant.previous.occupation'),
                                          ('res_id', '=', prev_occupation.id)])
                    for occupation_attachment in occupation_attachments:
                        emp_occupation_attachment = \
                            occupation_attachment.copy()
                        emp_occupation_attachment.write({
                            'res_model': 'employee.previous.occupation',
                            'res_id': occupation_id.id})
                for relative in self.env['applicant.relative'].search([
                        ('applicant_id', '=', applicant.id)]):
                    relative_id = self.env['employee.relative'].create({
                        'relative_type': relative.relative_type,
                        'name': relative.name,
                        'birthday': relative.birthday,
                        'place_of_birth': relative.place_of_birth,
                        'occupation': relative.occupation,
                        'gender': relative.gender,
                        'employee_id': res.get('res_id', False)})
                    relative_attachments =\
                        attch_obj.search([('res_model', '=',
                                           'applicant.relative'),
                                          ('res_id', '=', relative.id)])
                    for relative_attachment in relative_attachments:
                        emp_relative_attachment = relative_attachment.copy()
                        emp_relative_attachment.write({
                            'res_model': 'employee.relative',
                            'res_id': relative_id.id})
                for education in self.env['applicant.education'].search(
                        [('applicant_id', '=', applicant.id)]):
                    education_id = self.env['employee.education'].create({
                        'from_date': education.from_date,
                        'to_date': education.to_date,
                        'education_rank': education and
                        education.education_rank,
                        'school_name': education.school_name,
                        'grade': education.grade,
                        'field': education.field,
                        'illiterate': education.illiterate,
                        'edu_type': education.edu_type,
                        'country_id': education.country_id and
                        education.country_id.id,
                        'state_id': education.state_id and
                        education.state_id.id,
                        'province': education.province,
                        'employee_id': res.get('res_id', False)})
                    education_attachments =\
                        attch_obj.search([('res_model', '=',
                                           'applicant.education'),
                                          ('res_id', '=', education.id)])
                    for education_attachment in education_attachments:
                        emp_education_attachment = education_attachment.copy()
                        emp_education_attachment.write({
                            'res_model': 'employee.education',
                            'res_id': education_id.id})
                for prev_travel in applicant_trav_obj.search([
                        ('applicant_id', '=', applicant.id)]):
                    prev_travel_id = emp_trav_obj.create({
                        'from_date': prev_travel.from_date,
                        'to_date': prev_travel.to_date,
                        'location': prev_travel.location,
                        'reason': prev_travel.reason,
                        'employee_id': res.get('res_id', False)})
                    prev_travel_attach =\
                        attch_obj.search([('res_model', '=',
                                           'applicant.previous.travel'),
                                          ('res_id', '=', prev_travel.id)])
                    for prev_travel_attachment in prev_travel_attach:
                        emp_prev_travel_attachment =\
                            prev_travel_attachment.copy()
                        emp_prev_travel_attachment.write({
                            'res_model': 'employee.previous.travel',
                            'res_id': prev_travel_id.id})
                for language in self.env['applicant.language'].search([
                        ('applicant_id', '=', applicant.id)]):
                    language_id = self.env['employee.language'].create({
                        'language': language.language,
                        'read_lang': language.read_lang,
                        'write_lang': language.write_lang,
                        'speak_lang': language.speak_lang,
                        'mother_tongue': language.mother_tongue,
                        'employee_id': res.get('res_id', False)})
                    language_attachments = \
                        attch_obj.search([('res_model', '=',
                                           'applicant.language'),
                                          ('res_id', '=', language.id)])
                    for language_attachment in language_attachments:
                        emp_language_attachment = language_attachment.copy()
                        emp_language_attachment.write({'res_model':
                                                       'employee.language',
                                                       'res_id':
                                                       language_id.id})
        return res


class ApplicantMedicalDetails(models.Model):

    _name = "hr.applicant.medical.details"
    _description = "Applicant Medical Details"
    _rec_name = 'medical_examination'

    medical_examination = fields.Char('Medical Examination')
    vital_sign = fields.Char('Vital sign')
    date = fields.Date('Date', default=fields.Date.context_today,
                       readonly=True)
    doc_comment = fields.Char('Doctor’s Comments')

    head_face_scalp = fields.Selection([('Abnormal', 'Abnormal'),
                                        ('Normal', 'Normal')],
                                       'Head, Face, Scalp')
    nose_sinuses = fields.Selection([('Abnormal', 'Abnormal'),
                                     ('Normal', 'Normal')], 'Nose/Sinuses')
    mouth_throat = fields.Selection([('Abnormal', 'Abnormal'),
                                     ('Normal', 'Normal')], 'Mouth/Throat')
    ears_tms = fields.Selection([('Abnormal', 'Abnormal'),
                                 ('Normal', 'Normal')], 'Ears/TMs')
    eyes_pupils_ocular = fields.Selection([('Abnormal', 'Abnormal'),
                                           ('Normal', 'Normal')],
                                          'Eyes/Pupils/Ocular Motility')
    heart_vascular_system = fields.Selection([('Abnormal', 'Abnormal'),
                                              ('Normal', 'Normal')],
                                             'Heart/Vascular System')
    lungs = fields.Selection([('Abnormal', 'Abnormal'), ('Normal', 'Normal')],
                             'Lungs')
    abdomen_hernia = fields.Selection([('Abnormal', 'Abnormal'),
                                       ('Normal', 'Normal')], 'Abdomen/Hernia')
    msk_strengh = fields.Selection([('Abnormal', 'Abnormal'),
                                    ('Normal', 'Normal')], 'MSK-Strength')
    neurological = fields.Selection([('Abnormal', 'Abnormal'),
                                     ('Normal', 'Normal')],
                                    'Neurological (Reflexes, Sensation)')
    glasses_needed = fields.Boolean('Glasses Needed?')
    urine_drug_serene = fields.Selection([('Negative', 'Negative'),
                                          ('Positive', 'Positive')],
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

    applicant_id = fields.Many2one('hr.applicant', 'Applicant Ref',
                                   ondelete='cascade')
    active = fields.Boolean(string='Active', default=True)
    blood_name = fields.Selection([('A', 'A'), ('B', 'B'), ('O', 'O'),
                                   ('AB', 'AB')], "Blood Type")
    blood_type = fields.Selection([('+', '+'), ('-', '-')], 'Blood Type')

    @api.model
    def create(self, vals):
        if (self._context.get('active_model') == 'hr.applicant' and
                self._context.get('active_id')):
            vals.update({'applicant_id': self._context.get('active_id')})
        return super(ApplicantMedicalDetails, self).create(vals)


class ApplicantPreviousOccupation(models.Model):

    _name = "applicant.previous.occupation"
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
    applicant_id = fields.Many2one('hr.applicant', 'Applicant Ref',
                                   ondelete='cascade')
    email = fields.Char('Email')

    @api.model
    def create(self, vals):
        if (self._context.get('active_model') == 'hr.applicant' and
                self._context.get('active_id')):
            vals.update({'applicant_id': self._context.get('active_id')})
        return super(ApplicantPreviousOccupation, self).create(vals)

    @api.onchange('from_date', 'to_date')
    def onchange_date(self):
        if self.to_date and \
                datetime.strptime(self.to_date, DF) >= datetime.today():
            warning = {'title': _('User Alert !'),
                       'message': _('To date must be less than today!')}
            self.to_date = False
            return {'warning': warning}
        if self.from_date and self.to_date and self.from_date > self.to_date:
            warning = {'title': _('User Alert !'),
                       'message': _('To Date %s must be greater than\
                            From Date %s !') % (self.to_date, self.from_date)}
            self.to_date = False
            return {'warning': warning}


class ApplicantRelative(models.Model):

    _name = 'applicant.relative'
    _description = "Applicant Relatives"
    _rec_name = 'name'

    relative_type = fields.Selection([('Aunty', 'Aunty'),
                                      ('Brother', 'Brother'),
                                      ('Daughter', 'Daughter'),
                                      ('Father', 'Father'),
                                      ('Husband', 'Husband'),
                                      ('Mother', 'Mother'),
                                      ('Sister', 'Sister'), ('Son', 'Son'),
                                      ('Uncle', 'Uncle'),
                                      ('Wife', 'Wife'), ('Other', 'Other')],
                                     string='Relative Type', required=True)
    name = fields.Char(string='Name', size=128, required=True)
    birthday = fields.Date(string='Date of Birth')
    place_of_birth = fields.Char(string='Place of Birth', size=128)
    occupation = fields.Char(string='Occupation', size=128)
    gender = fields.Selection([('Male', 'Male'), ('Female', 'Female')],
                              string='Gender', required=False)
    active = fields.Boolean(string='Active', default=True)
    applicant_id = fields.Many2one('hr.applicant', 'Applicant Ref',
                                   ondelete='cascade')

    @api.onchange('birthday')
    def onchange_birthday(self):
        if self.birthday and \
                datetime.strptime(self.birthday, DF) >= datetime.today():
            warning = {'title': _('User Alert !'),
                       'message': _('Date of Birth must be less than today!')}
            self.birthday = False
            return {'warning': warning}

    @api.onchange('relative_type')
    def onchange_relative_type(self):
        if self.relative_type:
            if self.relative_type in ('Brother', 'Father', 'Husband',
                                      'Son', 'Uncle'):
                self.gender = 'Male'
            elif self.relative_type in ('Mother', 'Sister', 'Wife', 'Aunty'):
                self.gender = 'Female'
            else:
                self.gender = ''
        if self.applicant_id and not self.relative_type:
            warning = {'title': _('Warning!'),
                       'message': _('Please select Relative Type!'), }
            return {'gender': False, 'warning': warning}

    @api.model
    def create(self, vals):
        if (self._context.get('active_model') == 'hr.applicant' and
                self._context.get('active_id')):
            vals.update({'applicant_id': self._context.get('active_id')})
        return super(ApplicantRelative, self).create(vals)


class ApplicantEducation(models.Model):
    _name = "applicant.education"
    _description = "Applicant Education"
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
    applicant_id = fields.Many2one('hr.applicant', 'Applicant Ref',
                                   ondelete='cascade')
    edu_type = fields.Selection([('Local', 'Local'), ('Abroad', 'Abroad')],
                                string='School Location', default="Local")
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
        if (self._context.get('active_model') == 'hr.applicant' and
                self._context.get('active_id')):
            vals.update({'applicant_id': self._context.get('active_id')})
        return super(ApplicantEducation, self).create(vals)

    @api.onchange('from_date', 'to_date')
    def onchange_date(self):
        if self.to_date and \
                datetime.strptime(self.to_date, DF) >= datetime.today():
            warning = {'title': _('User Alert !'),
                       'message': _('To date must be less than today!')}
            self.to_date = False
            return {'warning': warning}
        if self.from_date and self.to_date and self.from_date > self.to_date:
            warning = {'title': _('User Alert !'),
                       'message': _('To Date must be greater than\
                        From Date !')}
            self.to_date = False
            return {'warning': warning}


class ApplicantPreviousTravel(models.Model):
    _name = "applicant.previous.travel"
    _description = "Applicant Previous Travel"
    _rec_name = "from_date"
    _order = "from_date"

    from_date = fields.Date(string='From Date', required=True)
    to_date = fields.Date(string='To Date', required=True)
    location = fields.Char(string='Location', size=128, required=True)
    reason = fields.Char('Reason', required=True)
    active = fields.Boolean(string='Active', default=True)
    applicant_id = fields.Many2one('hr.applicant', 'Applicant Ref',
                                   ondelete='cascade')

    @api.model
    def create(self, vals):
        if (self._context.get('active_model') == 'hr.applicant' and
                self._context.get('active_id')):
            vals.update({'applicant_id': self._context.get('active_id')})
        return super(ApplicantPreviousTravel, self).create(vals)

    @api.onchange('from_date', 'to_date')
    def onchange_date(self):
        if self.to_date and \
                datetime.strptime(self.to_date, DF) >= datetime.today():
            warning = {'title': _('User Alert !'),
                       'message': _('To date must be less than today!')}
            self.to_date = False
            return {'warning': warning}
        if self.from_date and self.to_date and self.from_date > self.to_date:
            warning = {'title': _('User Alert !'),
                       'message': _('To Date must be greater than From Date!')}
            self.to_date = False
            return {'warning': warning}


class ApplicantLanguage(models.Model):
    _name = "applicant.language"
    _description = "Applicant Language"
    _rec_name = "language"

    language = fields.Char('Language', required=True)
    read_lang = fields.Selection([('Excellent', 'Excellent'), ('Good', 'Good'),
                                  ('Poor', 'Poor')], string='Read')
    write_lang = fields.Selection([('Excellent', 'Excellent'),
                                   ('Good', 'Good'),
                                   ('Poor', 'Poor')], string='Write')
    speak_lang = fields.Selection([('Excellent', 'Excellent'),
                                   ('Good', 'Good'), ('Poor', 'Poor')],
                                  string='Speak')
    active = fields.Boolean(string='Active', default=True)
    applicant_id = fields.Many2one('hr.applicant', 'Applicant Ref',
                                   ondelete='cascade')
    mother_tongue = fields.Boolean('Mother Tongue')

    @api.constrains('mother_tongue')
    def _check_mother_tongue(self):
        if self.mother_tongue and self.applicant_id:
            language_rec = self.search([('applicant_id', '=',
                                         self.applicant_id.id),
                                        ('mother_tongue', '=', True),
                                        ('id', '!=', self.id)], limit=1)
            if language_rec:
                raise ValidationError(_("If you want to set '%s' as a mother \
                            tongue, first you have to uncheck mother tongue \
                            in '%s' language.") % (self.language,
                                                   language_rec.language))

    @api.model
    def create(self, vals):
        if self._context.get('active_model') == 'hr.applicant' and \
                self._context.get('active_id'):
            vals.update({'applicant_id': self._context.get('active_id')})
        return super(ApplicantLanguage, self).create(vals)
