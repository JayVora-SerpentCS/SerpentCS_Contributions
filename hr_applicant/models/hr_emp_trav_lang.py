from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class EmployeePreviousTravel(models.Model):
    _name = "employee.previous.travel"
    _description = "Employee Previous Travel"
    _rec_name = "from_date"
    _order = "from_date"

    from_date = fields.Date(string="From Date", required=True)
    to_date = fields.Date(string="To Date", required=True)
    location = fields.Char(string="Location", size=128, required=True)
    reason = fields.Char("Reason", required=True)
    active = fields.Boolean(string="Active", default=True)
    employee_id = fields.Many2one("hr.employee", "Employee Ref", ondelete="cascade")

    @api.model
    def create(self, vals):
        if self._context.get("active_model") == "hr.employee" and self._context.get(
            "active_id"
        ):
            vals.update({"employee_id": self._context.get("active_id")})
        return super(EmployeePreviousTravel, self).create(vals)

    @api.onchange("from_date", "to_date")
    def _onchange_date(self):
        if self.to_date and self.to_date >= datetime.today():

            warning = {
                "title": _("User Alert !"),
                "message": _("To date must be less than today !"),
            }
            self.to_date = False
            return {"warning": warning}
        if self.from_date and self.to_date and self.from_date > self.to_date:
            warning = {
                "title": _("User Alert !"),
                "message": _("To Date  must be greater than From Date  !"),
            }
            self.to_date = False
            return {"warning": warning}


class EmployeeLanguage(models.Model):
    _name = "employee.language"
    _description = "Employee Language"
    _rec_name = "language"
    _order = "id desc"

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
    employee_id = fields.Many2one("hr.employee", "Employee Ref", ondelete="cascade")
    mother_tongue = fields.Boolean("Mother Tongue")

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
                        "If you want to set '%s' \
                    as a mother tongue, first you have to uncheck mother \
                    tongue in '%s' language."
                    )
                    % (self.language, language_rec.language)
                )

    @api.model
    def create(self, vals):
        if self._context.get("active_model") == "hr.employee" and self._context.get(
            "active_id"
        ):
            vals.update({"employee_id": self._context.get("active_id")})
        return super(EmployeeLanguage, self).create(vals)
