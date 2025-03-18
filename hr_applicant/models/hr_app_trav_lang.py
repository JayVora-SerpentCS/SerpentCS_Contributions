from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _

SELECTION_LANGUAGE = [("Excellent", "Excellent"), ("Good", "Good"), ("Poor", "Poor")]

 
class ApplicantPreviousTravel(models.Model):
    _name = "applicant.previous.travel"
    _description = "Applicant Previous Travel"
    _rec_name = "location"
    _order = "from_date"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    from_date = fields.Date(required=True)
    to_date = fields.Date(required=True)
    location = fields.Char(required=True)
    reason = fields.Char(required=True)
    active = fields.Boolean(default=True)
    applicant_id = fields.Many2one("hr.applicant", "Applicant Ref", ondelete="cascade")

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        active_id = self._context.get("active_id")
        if (defaults.get("applicant_id") == False) or (defaults.get("applicant_id") != active_id):
            defaults.update({"applicant_id": active_id})
        return defaults

    @api.onchange("from_date", "to_date")
    def _onchange_date(self):
        """Give user alert for from date and to date"""
        message = False
        if self.to_date and self.to_date >= fields.Date.today():
            return {"warning": {
                    "title": _("User Alert !"),
                    "message" : _("To date should be prior to the current date!")
                }}
        elif self.from_date and self.to_date and self.from_date > self.to_date:
            return {"warning": {
                    "title": _("User Alert !"),
                    "message" : _("From Date should be prior to the To Date!")
                }}

    @api.constrains('from_date', 'to_date')
    def check_date(self):
        for rec in self:
            if (rec.from_date and rec.to_date) >= (fields.Date.today()):
                raise ValidationError(_("To date should be prior to the current date!"))
            elif (rec.from_date and rec.to_date) and (rec.from_date > rec.to_date):
                raise ValidationError(_("From Date should be prior to the To Date!"))


class ApplicantLanguage(models.Model):
    _name = "applicant.language"
    _description = "Applicant Language"
    _rec_name = "language"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    language = fields.Many2one("res.lang", required=True)

    read_lang = fields.Selection(SELECTION_LANGUAGE, "Read")
    write_lang = fields.Selection(SELECTION_LANGUAGE, "Write")
    speak_lang = fields.Selection(SELECTION_LANGUAGE, "Speak")

    active = fields.Boolean(default=True)
    applicant_id = fields.Many2one("hr.applicant", "Applicant Ref", ondelete="cascade")
    mother_tongue = fields.Boolean()

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        active_id = self._context.get("active_id")
        if (defaults.get("applicant_id") == False) or (defaults.get("applicant_id") != active_id):
            defaults.update({"applicant_id": active_id})
        return defaults

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
                        "If you want to set '%(lang)s' as a mothertongue "
                        "first uncheck mothertongue in '%(lang1)s' language"
                    )
                    % {"lang": self.language, "lang1": language_rec.language}
                )
