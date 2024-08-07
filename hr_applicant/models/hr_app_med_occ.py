from odoo import api, fields, models
from odoo.tools.translate import _

STATUS_SELECTION = [("Abnormal", "Abnormal"), ("Normal", "Normal")]


class ApplicantMedicalDetails(models.Model):
    _name = "hr.applicant.medical.details"
    _description = "Applicant Medical Details"
    _rec_name = "medical_examination"

    medical_examination = fields.Char("Medical Examination")
    vital_sign = fields.Char("Vital sign")
    date = fields.Date("Date", default=fields.Date.context_today, readonly=True)
    doc_comment = fields.Char("Doctor’s Comments")
    head_face_scalp = fields.Selection(STATUS_SELECTION, "Head, Face, Scalp")
    nose_sinuses = fields.Selection(STATUS_SELECTION, "Nose/Sinuses")
    mouth_throat = fields.Selection(STATUS_SELECTION, "Mouth/Throat")
    ears_tms = fields.Selection(STATUS_SELECTION, "Ears/TMs")
    eyes_pupils_ocular = fields.Selection(STATUS_SELECTION, "Eyes/Pupils/Ocular Motility")
    heart_vascular_system = fields.Selection(STATUS_SELECTION, "Heart/Vascular System")
    lungs = fields.Selection(STATUS_SELECTION, "Lungs")
    abdomen_hernia = fields.Selection(STATUS_SELECTION, "Abdomen/Hernia")
    msk_strengh = fields.Selection(STATUS_SELECTION, "MSK-Strength")
    neurological = fields.Selection(STATUS_SELECTION, "Neurological (Reflexes, Sensation)")
    glasses_needed = fields.Boolean("Glasses Needed?")
    urine_drug_serene = fields.Selection(
        [("Negative", "Negative"), ("Positive", "Positive")], "Urine Drug Serene"
    )
    fit_for_full_duty = fields.Boolean("Fully Fit for Duty?")

    good_health = fields.Boolean("Good Health?")
    serious_illness = fields.Boolean("Series Illness or Disease?")
    broken_bones = fields.Boolean("Broken Bones or Surgery?")
    medications = fields.Boolean("Medications at this time?")
    serious_wound = fields.Boolean("Seriously Wounded?")
    allergic = fields.Boolean("Allergic to any medication?")
    epilepsy = fields.Boolean("Epilepsy")
    history_drug_use = fields.Boolean("Any History of drug use?")

    applicant_id = fields.Many2one("hr.applicant", "Applicant Ref", ondelete="cascade")
    active = fields.Boolean(string="Active", default=True)
    blood_name = fields.Selection(
        [("A", "A"), ("B", "B"), ("O", "O"), ("AB", "AB")], "Blood Type"
    )
    blood_type = fields.Selection([("+", "+"), ("-", "-")], "Blood Type")

    @api.model_create_multi
    def create(self, vals_list):
        if self._context.get("active_model") == "hr.applicant" and self._context.get(
                "active_id"):
            for vals in vals_list:
                vals.update({"applicant_id": self._context.get("active_id")})
        return super(ApplicantMedicalDetails, self).create(vals_list)


class ApplicantPreviousOccupation(models.Model):
    _name = "applicant.previous.occupation"
    _description = "Applicants Previous Occupation"
    _order = "to_date desc"
    _rec_name = "position"

    from_date = fields.Date(string="From Date", required=True)
    to_date = fields.Date(string="To Date", required=True)
    position = fields.Char(string="Position", required=True)
    organization = fields.Char(string="Organization")
    ref_name = fields.Char(string="Reference Name")
    ref_position = fields.Char(string="Reference Position")
    ref_phone = fields.Char(string="Reference Phone")
    active = fields.Boolean(string="Active", default=True)
    applicant_id = fields.Many2one("hr.applicant", "Applicant Ref", ondelete="cascade")
    email = fields.Char("Email")

    @api.model_create_multi
    def create(self, vals_list):
        if self._context.get("active_model") == "hr.applicant" and self._context.get(
            "active_id"
        ):
            vals_list.update({"applicant_id": self._context.get("active_id")})
        return super(ApplicantPreviousOccupation, self).create(vals_list)

    @api.onchange("from_date", "to_date")
    def _onchange_date(self):
        """Give user alert for from date and to date"""
        warning = {
            "title": _("User Alert !"),
        }
        message = False
        if self.to_date and self.to_date >= fields.Date.today():
            message = _("To date must be less than today!")
        elif self.from_date and self.to_date and self.from_date > self.to_date:
            message = _("To Date must be greater than From Date!")
        if message:
            warning.update({"message": message})
            return {"warning": warning}
