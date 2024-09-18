from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _

SELECTION_LANGUAGE = [("Excellent", "Excellent"), ("Good", "Good"), ("Poor", "Poor")]


class ApplicantPreviousTravel(models.Model):
    _name = "applicant.previous.travel"
    _description = "Applicant Previous Travel"
    _rec_name = "from_date"
    _order = "from_date"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    from_date = fields.Date(string="From Date", required=True)
    to_date = fields.Date(string="To Date", required=True)
    location = fields.Char(string="Location", required=True)
    reason = fields.Char("Reason", required=True)
    active = fields.Boolean(string="Active", default=True)
    applicant_id = fields.Many2one("hr.applicant", "Applicant Ref", ondelete="cascade")

    @api.onchange("from_date", "to_date")
    def _onchange_date(self):
        """Give user alert for from date and to date"""
        warning = {
            "title": _("User Alert !"),
        }
        message = False
        if self.to_date and self.to_date >= fields.Date.today():
            message = _("To date should be prior to the current date!")
        elif self.from_date and self.to_date and self.from_date > self.to_date:
            message = _("From Date should be prior to the To Date!")
        if message:
            warning.update({"message": message})
            return {"warning": warning}


class ApplicantLanguage(models.Model):
    _name = "applicant.language"
    _description = "Applicant Language"
    _rec_name = "language"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    
    language = fields.Many2one("res.lang", required=True)

    read_lang = fields.Selection(SELECTION_LANGUAGE, "Read")
    write_lang = fields.Selection(SELECTION_LANGUAGE, "Write")
    speak_lang = fields.Selection(SELECTION_LANGUAGE, "Speak")

    active = fields.Boolean(string="Active", default=True)
    applicant_id = fields.Many2one("hr.applicant", "Applicant Ref", ondelete="cascade")
    mother_tongue = fields.Boolean("Mother Tongue")

    @api.constrains("mother_tongue")
    def _check_mother_tongue(self):
        self.ensure_one()
        if self.mother_tongue and self.applicant_id:
            language_rec = self.search(
                [
                    ("applicant_id", "=", self.applicant_id.id),
                    ("mother_tongue", "=", True),
                    ("id", "!=", self.id),
                ],
                limit=1,
            )
            if language_rec:
                raise ValidationError(
                    _(
                        "If you want to set '%s' as a mother tongue "
                        "first uncheck mother tongue in '%s' language"
                    )
                    % (self.language.name, language_rec.language.name)
                )
