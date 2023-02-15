# See LICENSE file for full copyright and licensing details.

from odoo.tests import common


class HRGradeTestCase(common.TransactionCase):

    def setup(self):
        super().setup()

    def test_hr_grade_rank(self):
        rank = self.env["rank.rank"].create({
            "name": "Test HR Rank B",
            "description": "Test Description of HR Rank.",
            "salary_range": "30000",
        })
        grade = self.env["grade.grade"].create({
            "name": "Test Hr Grade",
            "description": "Grade Details",
            "rank_ids": [(
                0,
                0,
                {
                    "name": "Test HR Rank",
                    "description": "Description of HR Rank.",
                    "salary_range": "30000",
                },
            )]
        })
        employee_rec = self.env["hr.employee"].sudo().create(
            {
                "name": "HR Grade Test Employee",
                "grade_id": grade.id,
                "rank_id": rank.id,
            }
        )
        self.assertEqual(grade.id, employee_rec.grade_id.id)
        self.assertEqual(rank.id, employee_rec.rank_id.id)
