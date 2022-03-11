# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class RankRank(models.Model):
    _name = "rank.rank"
    _description = "Rank"

    name = fields.Char()
    description = fields.Text()
    salary_range = fields.Text()
    active = fields.Boolean('Active',default=True)

    _sql_constraints=[('name_uniq', 'unique(name)',"Rank should be unique")]


class GradeGrade(models.Model):
    _name = "grade.grade"
    _description = "Grade"

    name = fields.Char()
    description = fields.Text()
    rank_ids=fields.Many2many("rank.rank","rel_grade_rank","grade_id","rank_id","Ranks")
    active = fields.Boolean('Active',default=True)


class HrEmployee(models.Model):

    _inherit = "hr.employee"

    grade_id = fields.Many2one("grade.grade", "Grade")
    rank_id = fields.Many2one("rank.rank", "Rank")
    

    @api.onchange("grade_id")
    def _onchange_grade(self):
        res = {}
        if self.grade_id:
            self.rank_id = False
            res["domain"] = {"rank_id": [
                ("id", "in", self.grade_id.rank_ids.ids)]}
        return res
