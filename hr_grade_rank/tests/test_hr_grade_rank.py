# See LICENSE file for full copyright and licensing details.

from odoo.tests import common


class HRGradeTestCase(common.TransactionCase):
    def setup(self):
        return super(HRGradeTestCase, self).setup()

    def tests_hr_grade_rank(self):
        self.rank_obj = self.env["rank.rank"]
        self.rank_id = self.rank_obj.create(
            {
                "name": "Test HR Rank",
                "description": "Test Description of HR Rank.",
                "salary_range": "30000",
            }
        )

        self.grade_obj = self.env["grade.grade"]
        self.grade_id = self.grade_obj.create(
            {
                "name": "Test Hr Grade",
                "description": "Grade Details",
                "rank_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Test HR Rank",
                            "description": "Description of HR Rank.",
                            "salary_range": "30000",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": "Test HR Rank A",
                            "description": "Description of HR Rank A.",
                            "salary_range": "20000",
                        },
                    ),
                ],
            }
        )

        self.rank_id.write({"grade_id": self.grade_id.id})

        self.employee_obj = self.env["hr.employee"]
        self.employee_id = self.employee_obj.create(
            {
                "name": "HR Grade Test Employee",
                "grade_id": self.grade_id.id,
                "rank_id": self.rank_id.id,
            }
        )
