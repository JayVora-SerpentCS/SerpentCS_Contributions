from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class ApplicantRelative(models.Model):
    _name = "applicant.relative"
    _description = "Applicant Relatives"
    _inherit = ["mail.thread", "mail.activity.mixin"]

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
        required=True,
    )
    name = fields.Char(required=True)
    birthday = fields.Date(string="Date of Birth")
    place_of_birth = fields.Char()
    occupation = fields.Char()
    gender = fields.Selection([("Male", "Male"), ("Female", "Female")])
    active = fields.Boolean(default=True)
    applicant_id = fields.Many2one("hr.applicant", "Applicant Ref", ondelete="cascade")

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        if (defaults.get("applicant_id") == False) or (defaults.get("applicant_id") != self._context.get("active_id")):
            defaults.update({"applicant_id": self._context.get("active_id")})
        return defaults

    @api.onchange("birthday")
    def _onchange_birthday(self):
        if self.birthday and self.birthday >= fields.Date.today():
            warning = {
                "title": _("User Alert !"),
                "message": _("Date of Birth should be prior of current Date!"),
            }
            self.birthday = False
            return {"warning": warning}

    @api.onchange("relative_type")
    def _onchange_relative_type(self):
        male_relative = {"Brother", "Father", "Husband", "Son", "Uncle"}
        female_relative = {"Mother", "Sister", "Wife", "Aunty", "Daughter"}
        if self.relative_type:
            self.gender = ""
            if self.relative_type in male_relative:
                self.gender = "Male"
            elif self.relative_type in female_relative:
                self.gender = "Female"
        # Already relative_type field is required no need to add tehe warning.
        # if self.applicant_id and not self.relative_type:
        #     warning = {
        #         "title": _("Warning!"),
        #         "message": _("Please select Relative Type!"),
        #     }
        #     return {"gender": False, "warning": warning}


class ApplicantEducation(models.Model):
    _name = "applicant.education"
    _description = "Applicant Education"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "grade"
    _order = "from_date"

    from_date = fields.Date()
    to_date = fields.Date()
    education_rank = fields.Char(string="Education Rank")
    school_name = fields.Char(string="School Name")
    grade = fields.Char(string="Education Field")
    field = fields.Char(string="Field of Education")
    illiterate = fields.Boolean(string="Is Illiterate?")
    active = fields.Boolean(default=True)
    applicant_id = fields.Many2one("hr.applicant", "Applicant Ref", ondelete="cascade")
    edu_type = fields.Selection(
        [("Local", "Local"), ("Abroad", "Abroad")],
        string="School Location",
        default="Local",
    )
    country_id = fields.Many2one("res.country", "Country")
    state_id = fields.Many2one("res.country.state", "State")
    province = fields.Char()

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        if (defaults.get("applicant_id") == False) or (defaults.get("applicant_id") != self._context.get("active_id")):
            defaults.update({"applicant_id": self._context.get("active_id")})
        return defaults

    @api.onchange("edu_type")
    def _onchange_edu_type(self):
        for rec in self:
            rec.country_id = False if rec.edu_type == "Local" else rec.country_id
            rec.province = rec.state_id = (
                False if rec.edu_type != "Local" else rec.province
            )

    @api.onchange("illiterate")
    def _onchange_illiterate(self):
        for rec in self:
            rec.from_date = rec.to_date = rec.country_id = rec.state_id = False
            rec.education_rank = (
                rec.school_name
            ) = rec.grade = rec.field = rec.edu_type = rec.province = ""

    @api.constrains("from_date", "to_date")
    def check_date(self):
        for rec in self:
            if (rec.from_date and rec.to_date) >= (fields.Date.today()):
                raise UserError(_("To date should be prior to the current date!"))
            elif (rec.from_date and rec.to_date) and (rec.from_date > rec.to_date):
                raise UserError(_("From Date should be prior to the To Date!"))
