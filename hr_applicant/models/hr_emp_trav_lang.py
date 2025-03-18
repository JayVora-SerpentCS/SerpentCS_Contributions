from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _

from .hr_app_trav_lang import SELECTION_LANGUAGE


class EmployeePreviousTravel(models.Model):
    _name = "employee.previous.travel"
    _description = "Employee Previous Travel"
    _rec_name = "from_date"
    _order = "from_date"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    from_date = fields.Date(required=True)
    to_date = fields.Date(required=True)
    location = fields.Char(required=True)
    reason = fields.Char(required=True)
    active = fields.Boolean(default=True)
    employee_id = fields.Many2one("hr.employee", "Employee Ref", ondelete="cascade")

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        if defaults.get("employee_id") == False:
            defaults.update({"employee_id": self._context.get("active_id")})
        return defaults

    @api.onchange("from_date", "to_date")
    def _onchange_date(self):
        warning = {
            "title": _("User Alert !"),
        }
        message = False
        if self.to_date and self.to_date >= datetime.today().date():
            message = _("To date should be prior to the current date!")
        elif self.from_date and self.to_date and self.from_date > self.to_date:
            message = _("From Date should be prior to the To Date!")
        if message:
            warning.update({"message": message})
            return {"warning": warning}


class EmployeeLanguage(models.Model):
    _name = "employee.language"
    _description = "Employee Language"
    _order = "id desc"
    _rec_name = "language"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    language = fields.Many2one("res.lang", required=True)

    read_lang = fields.Selection(SELECTION_LANGUAGE, "Read")
    write_lang = fields.Selection(SELECTION_LANGUAGE, "Write")
    speak_lang = fields.Selection(SELECTION_LANGUAGE, "Speak")
    active = fields.Boolean(default=True)
    mother_tongue = fields.Boolean()
    employee_id = fields.Many2one("hr.employee", "Employee Ref", ondelete="cascade")

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        if defaults.get("employee_id") == False:
            defaults.update({"employee_id": self._context.get("active_id")})
        return defaults

    @api.constrains("mother_tongue")
    def _check_mother_tongue(self):
        self.ensure_one()
        if self.mother_tongue and self.employee_id:
            language_rec = self.search(
                [
                    ("employee_id", "=", self.employee_id.id),
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
