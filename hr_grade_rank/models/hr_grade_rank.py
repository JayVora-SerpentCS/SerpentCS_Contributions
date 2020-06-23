# See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class RankRank(models.Model):
    _name = "rank.rank"

    name = fields.Char("Name")
    description = fields.Text("Description")
    salary_range = fields.Text("Salary Range")
    grade_id = fields.Many2one("grade.grade", "Grade")


class GradeGrade(models.Model):
    _name = "grade.grade"

    name = fields.Char("Name")
    description = fields.Text("Description")
    rank_ids = fields.One2many("rank.rank", "grade_id", "Ranks")


class HrEmployee(models.Model):

    _inherit = "hr.employee"

    grade_id = fields.Many2one("grade.grade", "Grade")
    rank_id = fields.Many2one("rank.rank", "Rank")

    @api.onchange("grade_id")
    def onchange_grade(self):
        res = {}
        if self.grade_id:
            self.rank_id = False
            res["domain"] = {"rank_id": [("id", "in", self.grade_id.rank_ids.ids)]}
        return res
