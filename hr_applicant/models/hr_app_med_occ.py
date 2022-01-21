from datetime import datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

class ApplicantMedicalDetails(models.Model):

    _name = "hr.applicant.medical.details"
    _description = "Applicant Medical Details"
    _rec_name = "medical_examination"

    medical_examination = fields.Char("Medical Examination")
    vital_sign = fields.Char("Vital sign")
    date = fields.Date(
        "Date", default=fields.Date.context_today, readonly=True)
    doc_comment = fields.Char("Doctor’s Comments")

    head_face_scalp = fields.Selection(
        [("Abnormal", "Abnormal"), ("Normal", "Normal")], "Head, Face, Scalp"
    )
    nose_sinuses = fields.Selection(
        [("Abnormal", "Abnormal"), ("Normal", "Normal")], "Nose/Sinuses"
    )
    mouth_throat = fields.Selection(
        [("Abnormal", "Abnormal"), ("Normal", "Normal")], "Mouth/Throat"
    )
    ears_tms = fields.Selection(
        [("Abnormal", "Abnormal"), ("Normal", "Normal")], "Ears/TMs"
    )
    eyes_pupils_ocular = fields.Selection(
        [("Abnormal", "Abnormal"), ("Normal", "Normal")
         ], "Eyes/Pupils/Ocular Motility"
    )
    heart_vascular_system = fields.Selection(
        [("Abnormal", "Abnormal"), ("Normal", "Normal")], "Heart/Vascular System"
    )
    lungs = fields.Selection(
        [("Abnormal", "Abnormal"), ("Normal", "Normal")], "Lungs")
    abdomen_hernia = fields.Selection(
        [("Abnormal", "Abnormal"), ("Normal", "Normal")], "Abdomen/Hernia"
    )
    msk_strengh = fields.Selection(
        [("Abnormal", "Abnormal"), ("Normal", "Normal")], "MSK-Strength"
    )
    neurological = fields.Selection(
        [("Abnormal", "Abnormal"), ("Normal", "Normal")],
        "Neurological (Reflexes, Sensation)",
    )
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

    applicant_id = fields.Many2one(
        "hr.applicant", "Applicant Ref", ondelete="cascade")
    active = fields.Boolean(string="Active", default=True)
    blood_name = fields.Selection(
        [("A", "A"), ("B", "B"), ("O", "O"), ("AB", "AB")], "Blood Type"
    )
    blood_type = fields.Selection([("+", "+"), ("-", "-")], "Blood Type")

    @api.model
    def create(self, vals):
        if self._context.get("active_model") == "hr.applicant" and self._context.get(
            "active_id"
        ):
            vals.update({"applicant_id": self._context.get("active_id")})
        return super(ApplicantMedicalDetails, self).create(vals)


class ApplicantPreviousOccupation(models.Model):

    _name = "applicant.previous.occupation"
    _description = "Recruite Previous Occupation"
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
    applicant_id = fields.Many2one(
        "hr.applicant", "Applicant Ref", ondelete="cascade")
    email = fields.Char("Email")

    @api.model
    def create(self, vals):
        if self._context.get("active_model") == "hr.applicant" and self._context.get(
            "active_id"
        ):
            vals.update({"applicant_id": self._context.get("active_id")})
        return super(ApplicantPreviousOccupation, self).create(vals)

    @api.onchange("from_date", "to_date")
    def _onchange_date(self):
      

        if (self.to_date  and self.to_date >= fields.Date.today()):
          
            warning = {
                "title": _("User Alert !"),
                "message": _("To date must be less than today!"),
            }
            self.to_date = False
            return {"warning": warning}
        if self.from_date and self.to_date and self.from_date > self.to_date:
            warning = {
                "title": _("User Alert !"),
                "message": _("To Date %s must be greater than From Date %s !")
                % (self.to_date, self.from_date),
            }
            self.to_date = False
            return {"warning": warning}
