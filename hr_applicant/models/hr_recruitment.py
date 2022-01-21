# See LICENSE file for full copyright and licensing details.

from datetime import datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _



class Applicant(models.Model):
    _inherit = "hr.applicant"
    _description = "Applicant"

    @api.depends("medical_ids")
    def _compute_no_of_medical(self):
        for rec in self:
            rec.no_of_medical = len(rec.medical_ids.ids)
            rec.no_of_medical1 = len(rec.medical_ids.ids)

    @api.depends("prev_occu_ids")
    def _compute_no_of_prev_occu(self):
        for rec in self:
            rec.no_of_prev_occu = len(rec.prev_occu_ids.ids)

    @api.depends("relative_ids")
    def _compute_no_of_relative(self):
        for rec in self:
            rec.no_of_relative = len(rec.relative_ids.ids)

    @api.depends("education_ids")
    def _compute_no_of_education(self):
        for rec in self:
            rec.no_of_education = len(rec.education_ids.ids)

    @api.depends("prev_travel_ids")
    def _compute_no_of_prev_travel(self):
        for rec in self:
            rec.no_of_prev_travel = len(rec.prev_travel_ids.ids)

    @api.depends("lang_ids")
    def _compute_no_of_lang(self):
        for rec in self:
            rec.no_of_lang = len(rec.lang_ids.ids)

    medical_ids = fields.One2many(
        "hr.applicant.medical.details", "applicant_id", "Medical Ref."
    )
    no_of_medical = fields.Integer(
        "No of Medical Detials", compute="_compute_no_of_medical", readonly=True
    )
    no_of_medical1 = fields.Integer(
        "No of Medical Detials", compute="_compute_no_of_medical", readonly=True
    )
    prev_occu_ids = fields.One2many(
        "applicant.previous.occupation", "applicant_id", "Prev. Occupation Ref."
    )
    no_of_prev_occu = fields.Integer(
        "No of Prev. Occupation", compute="_compute_no_of_prev_occu", readonly=True
    )
    relative_ids = fields.One2many(
        "applicant.relative", "applicant_id", "Relative Ref."
    )
    no_of_relative = fields.Integer(
        "No of Relative", compute="_compute_no_of_relative", readonly=True
    )
    education_ids = fields.One2many(
        "applicant.education", "applicant_id", "Education Ref."
    )
    no_of_education = fields.Integer(
        "No of Education", compute="_compute_no_of_education", readonly=True
    )
    prev_travel_ids = fields.One2many(
        "applicant.previous.travel", "applicant_id", "Previous Travel Ref."
    )
    no_of_prev_travel = fields.Integer(
        "No of Previous Travel", compute="_compute_no_of_prev_travel", readonly=True
    )
    lang_ids = fields.One2many(
        "applicant.language", "applicant_id", "Language Ref.")
    no_of_lang = fields.Integer(
        "No of Language", compute="_compute_no_of_lang", readonly=True
    )

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        ir_actions_report = self.env["ir.actions.report"]
        res = super(Applicant, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
        )
        reports = ir_actions_report.search(
            [("report_name", "=", "hr_applicant.applicant_profile")]
        )
        if reports and view_type != "form":
            new_reports = []
            for rec in res.get("toolbar", {}).get("print", []):
                if rec.get("id", False) not in reports.ids:
                    new_reports.append(rec)
            res.get("toolbar", {})["print"] = new_reports
        return res

    def create_employee_from_applicant(self):
        app_med_details_obj = self.env["hr.applicant.medical.details"]
        emp_med_details_obj = self.env["hr.employee.medical.details"]
        attachment_obj = self.env["ir.attachment"]
        app_prev_occ_obj = self.env["applicant.previous.occupation"]
        emp_prev_occ_obj = self.env["employee.previous.occupation"]
        app_rel_obj = self.env["applicant.relative"]
        emp_rel_obj = self.env["employee.relative"]
        app_edu_obj = self.env["applicant.education"]
        emp_edu_obj = self.env["employee.education"]
        app_tr_obj = self.env["applicant.previous.travel"]
        emp_tr_obj = self.env["employee.previous.travel"]
        app_lan_obj = self.env["applicant.language"]
        emp_lan_obj = self.env["employee.language"]

        res = super(Applicant, self).create_employee_from_applicant()
        data_dict = res.get("context")
        record_emp = self.env['hr.employee'].create({
            'name': data_dict.get("default_name"),
            'job_id': data_dict.get("default_job_id"),
            'job_title': data_dict.get("default_job_title"),
            'address_home_id': data_dict.get("address_home_id"),
            'department_id': data_dict.get("default_department_id"),
            'address_id': data_dict.get("default_address_id"),
            'work_email': data_dict.get("default_work_email"),
            'work_phone': data_dict.get("default_work_phone")})
        res["res_id"] = record_emp.id
        self.write({"emp_id": record_emp.id})
        if res.get("res_id", False):
            for applicant in self:
                for medical_detail in app_med_details_obj.search(
                    [("applicant_id", "=", applicant.id)]
                ):
                    medical_id = emp_med_details_obj.create(
                        {
                            "medical_examination": medical_detail.medical_examination,
                            "vital_sign": medical_detail.vital_sign,
                            "date": medical_detail.date,
                            "doc_comment": medical_detail.doc_comment,
                            "head_face_scalp": medical_detail.head_face_scalp,
                            "nose_sinuses": medical_detail.nose_sinuses,
                            "mouth_throat": medical_detail.mouth_throat,
                            "ears_tms": medical_detail.ears_tms,
                            "eyes_pupils_ocular": medical_detail.eyes_pupils_ocular,
                            "heart_vascular_system": medical_detail.heart_vascular_system,
                            "lungs": medical_detail.lungs,
                            "abdomen_hernia": medical_detail.abdomen_hernia,
                            "msk_strengh": medical_detail.msk_strengh,
                            "neurological": medical_detail.neurological,
                            "glasses_needed": medical_detail.glasses_needed,
                            "urine_drug_serene": medical_detail.urine_drug_serene,
                            "fit_for_full_duty": medical_detail.fit_for_full_duty,
                            "good_health": medical_detail.good_health,
                            "serious_illness": medical_detail.serious_illness,
                            "broken_bones": medical_detail.broken_bones,
                            "medications": medical_detail.medications,
                            "serious_wound": medical_detail.serious_wound,
                            "allergic": medical_detail.allergic,
                            "epilepsy": medical_detail.epilepsy,
                            "history_drug_use": medical_detail.history_drug_use,
                            # "employee_id": res.get("res_id", False),
                            "blood_name": medical_detail.blood_name,
                            "blood_type": medical_detail.blood_type,
                        }
                    )
                    medical_attachments = attachment_obj.search(
                        [
                            ("res_model", "=", "hr.applicant.medical.details"),
                            ("res_id", "=", medical_detail.id),
                        ]
                    )
                    for medical_attachment in medical_attachments:
                        emp_medical_attachment = medical_attachment.copy()
                        emp_medical_attachment.write(
                            {
                                "res_model": "hr.employee.medical.details",
                                "res_id": medical_id.id,
                            }
                        )
                for prev_occupation in app_prev_occ_obj.search(
                    [("applicant_id", "=", applicant.id)]
                ):
                    occupation_id = emp_prev_occ_obj.create(
                        {
                            "from_date": prev_occupation.from_date,
                            "to_date": prev_occupation.to_date,
                            "position": prev_occupation.position,
                            "organization": prev_occupation.organization,
                            "ref_name": prev_occupation.ref_name,
                            "ref_position": prev_occupation.ref_position,
                            "ref_phone": prev_occupation.ref_phone,
                            "employee_id": res.get("res_id", False),
                            "email": prev_occupation.email,
                        }
                    )
                    occupation_attachments = attachment_obj.search(
                        [
                            ("res_model", "=", "applicant.previous.occupation"),
                            ("res_id", "=", prev_occupation.id),
                        ]
                    )
                    for occupation_attachment in occupation_attachments:
                        emp_occupation_attachment = occupation_attachment.copy()
                        emp_occupation_attachment.write(
                            {
                                "res_model": "employee.previous.occupation",
                                "res_id": occupation_id.id,
                            }
                        )
                for relative in app_rel_obj.search(
                    [("applicant_id", "=", applicant.id)]
                ):
                    relative_id = emp_rel_obj.create(
                        {
                            "relative_type": relative.relative_type,
                            "name": relative.name,
                            "birthday": relative.birthday,
                            "place_of_birth": relative.place_of_birth,
                            "occupation": relative.occupation,
                            "gender": relative.gender,
                            "employee_id": res.get("res_id", False),
                        }
                    )
                    relative_attachments = attachment_obj.search(
                        [
                            ("res_model", "=", "applicant.relative"),
                            ("res_id", "=", relative.id),
                        ]
                    )
                    for relative_attachment in relative_attachments:
                        emp_relative_attachment = relative_attachment.copy()
                        emp_relative_attachment.write(
                            {"res_model": "employee.relative",
                                "res_id": relative_id.id}
                        )
                for education in app_edu_obj.search(
                    [("applicant_id", "=", applicant.id)]
                ):
                    education_id = emp_edu_obj.create(
                        {
                            "from_date": education.from_date,
                            "to_date": education.to_date,
                            "education_rank": education.education_rank,
                            "school_name": education.school_name,
                            "grade": education.grade,
                            "field": education.field,
                            "illiterate": education.illiterate,
                            "edu_type": education.edu_type,
                            "country_id": education.country_id
                            and education.country_id.id,
                            "state_id": education.state_id and education.state_id.id,
                            "province": education.province,
                            "employee_id": res.get("res_id", False),
                        }
                    )
                    education_attachments = attachment_obj.search(
                        [
                            ("res_model", "=", "applicant.education"),
                            ("res_id", "=", education.id),
                        ]
                    )
                    for education_attachment in education_attachments:
                        emp_education_attachment = education_attachment.copy()
                        emp_education_attachment.write(
                            {
                                "res_model": "employee.education",
                                "res_id": education_id.id,
                            }
                        )
                for prev_travel in app_tr_obj.search(
                    [("applicant_id", "=", applicant.id)]
                ):
                    prev_travel_id = emp_tr_obj.create(
                        {
                            "from_date": prev_travel.from_date,
                            "to_date": prev_travel.to_date,
                            "location": prev_travel.location,
                            "reason": prev_travel.reason,
                            "employee_id": res.get("res_id", False),
                        }
                    )
                    prev_travel_attachments = attachment_obj.search(
                        [
                            ("res_model", "=", "applicant.previous.travel"),
                            ("res_id", "=", prev_travel.id),
                        ]
                    )
                    for prev_travel_attachment in prev_travel_attachments:
                        emp_prev_travel_attachment = prev_travel_attachment.copy()
                        emp_prev_travel_attachment.write(
                            {
                                "res_model": "employee.previous.travel",
                                "res_id": prev_travel_id.id,
                            }
                        )
                for language in  app_lan_obj.search(
                    [("applicant_id", "=", applicant.id)]
                ):
                    language_id = emp_lan_obj.create(
                        {
                            "language": language.language,
                            "read_lang": language.read_lang,
                            "write_lang": language.write_lang,
                            "speak_lang": language.speak_lang,
                            "mother_tongue": language.mother_tongue,
                            "employee_id": res.get("res_id", False),
                        }
                    )
                    language_attachments = attachment_obj.search(
                        [
                            ("res_model", "=", "applicant.language"),
                            ("res_id", "=", language.id),
                        ]
                    )
                    for language_attachment in language_attachments:
                        emp_language_attachment = language_attachment.copy()
                        emp_language_attachment.write(
                            {"res_model": "employee.language",
                                "res_id": language_id.id}
                        )
        return res


