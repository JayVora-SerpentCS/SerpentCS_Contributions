
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class ApplicantPreviousTravel(models.Model):
    _name = "applicant.previous.travel"
    _description = "Applicant Previous Travel"
    _rec_name = "from_date"
    _order = "from_date"

    from_date = fields.Date(string="From Date", required=True)
    to_date = fields.Date(string="To Date", required=True)
    location = fields.Char(string="Location", size=128, required=True)
    reason = fields.Char("Reason", required=True)
    active = fields.Boolean(string="Active", default=True)
    applicant_id = fields.Many2one("hr.applicant", "Applicant Ref", ondelete="cascade")

    @api.model
    def create(self, vals):

        if self._context.get("active_model") == "hr.applicant" and self._context.get(
            "active_id"
        ):
            vals.update({"applicant_id": self._context.get("active_id")})
        return super(ApplicantPreviousTravel, self).create(vals)

    @api.onchange("from_date", "to_date")
    def _onchange_date(self):

        if self.to_date and self.to_date >= fields.Date.today():

            warning = {
                "title": _("User Alert !"),
                "message": _("To date must be less than today!"),
            }
            self.to_date = False
            return {"warning": warning}
        if self.from_date and self.to_date and self.from_date > self.to_date:
            warning = {
                "title": _("User Alert !"),
                "message": _("To Date must be greater than From Date!"),
            }
            self.to_date = False
            return {"warning": warning}


class ApplicantLanguage(models.Model):
    _name = "applicant.language"
    _description = "Applicant Language"
    _rec_name = "language"

    language = fields.Char("Language", required=True)
    read_lang = fields.Selection(
        [("Excellent", "Excellent"), ("Good", "Good"), ("Poor", "Poor")], string="Read"
    )
    write_lang = fields.Selection(
        [("Excellent", "Excellent"), ("Good", "Good"), ("Poor", "Poor")], string="Write"
    )
    speak_lang = fields.Selection(
        [("Excellent", "Excellent"), ("Good", "Good"), ("Poor", "Poor")], string="Speak"
    )
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
                        "If you want to set '%s' \
                    as a mother tongue, first you have to uncheck mother \
                    tongue in '%s' language."
                    )
                    % (self.language, language_rec.language)
                )

    @api.model
    def create(self, vals):
        if self._context.get("active_model") == "hr.applicant" and self._context.get(
            "active_id"
        ):
            vals.update({"applicant_id": self._context.get("active_id")})
        return super(ApplicantLanguage, self).create(vals)
