from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class EmployeeRelative(models.Model):

    _name = "employee.relative"
    _description = "Employee Relatives"
    _rec_name = "name"

    relative_type = fields.Selection(
        [
            ("Aunty", "Aunty"),
            ("Brother", "Brother"),
            ("Daughter", "Daughter"),
            ("Father", "Father"),
            ("Husband", "Husband"),
            ("Mother", "Mother"),
            ("Sister", "Sister"),
            ("Son", "Son"),
            ("Uncle", "Uncle"),
            ("Wife", "Wife"),
            ("Other", "Other"),
        ],
        string="Relative Type",
        required=True,
    )
    name = fields.Char(string="Name", size=128, required=True)
    birthday = fields.Date(string="Date of Birth")
    place_of_birth = fields.Char(string="Place of Birth", size=128)
    occupation = fields.Char(string="Occupation", size=128)
    gender = fields.Selection(
        [("Male", "Male"), ("Female", "Female")], string="Gender", required=False
    )
    active = fields.Boolean(string="Active", default=True)
    employee_id = fields.Many2one("hr.employee", "Employee Ref", ondelete="cascade")

    @api.onchange("birthday")
    def _onchange_birthday(self):
        if self.birthday and self.birthday >= datetime.today():

            warning = {
                "title": _("User Alert !"),
                "message": _("Date of Birth must be less than today!"),
            }
            self.birthday = False
            return {"warning": warning}

    @api.onchange("relative_type")
    def _onchange_relative_type(self):
        if self.relative_type:
            self.gender = ""
            if self.relative_type in ("Brother", "Father", "Husband", "Son", "Uncle"):
                self.gender = "Male"
            elif self.relative_type in ("Mother", "Sister", "Wife", "Aunty"):
                self.gender = "Female"
        if self.employee_id and not self.relative_type:
            warning = {
                "title": _("Warning!"),
                "message": _("Please select Relative Type!"),
            }
            return {"gender": False, "warning": warning}

    @api.model
    def create(self, vals):
        if self._context.get("active_model") == "hr.employee" and self._context.get(
            "active_id"
        ):
            vals.update({"employee_id": self._context.get("active_id")})
        return super(EmployeeRelative, self).create(vals)


class EmployeeEducation(models.Model):
    _name = "employee.education"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Employee Education"
    _rec_name = "from_date"
    _order = "from_date"

    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    education_rank = fields.Char("Education Rank")
    school_name = fields.Char(string="School Name", size=256)
    grade = fields.Char("Education Field/Major")
    field = fields.Char(string="Major/Field of Education", size=128)
    illiterate = fields.Boolean("Illiterate")
    active = fields.Boolean(string="Active", default=True)
    employee_id = fields.Many2one("hr.employee", "Employee Ref", ondelete="cascade")
    edu_type = fields.Selection(
        [("Local", "Local"), ("Abroad", "Abroad")], "School Location", default="Local"
    )
    country_id = fields.Many2one("res.country", "Country")
    state_id = fields.Many2one("res.country.state", "State")
    province = fields.Char("Province")

    @api.onchange("edu_type")
    def _onchange_edu_type(self):
        for rec in self:
            if rec.edu_type == "Local":
                rec.country_id = False
            else:
                rec.province = False
                rec.state_id = False

    @api.onchange("illiterate")
    def _onchange_illiterate(self):
        for rec in self:
            rec.from_date = False
            rec.to_date = False
            rec.education_rank = ""
            rec.school_name = ""
            rec.grade = ""
            rec.field = ""
            rec.edu_type = ""
            rec.country_id = False
            rec.state_id = False
            rec.province = ""

    @api.model
    def create(self, vals):
        if self._context.get("active_model") == "hr.employee" and self._context.get(
            "active_id"
        ):
            vals.update({"employee_id": self._context.get("active_id")})
        return super(EmployeeEducation, self).create(vals)

    @api.onchange("from_date", "to_date")
    def _onchange_date(self):
        to_date = self.to_date

        if self.to_date and self.to_date >= datetime.today():

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
