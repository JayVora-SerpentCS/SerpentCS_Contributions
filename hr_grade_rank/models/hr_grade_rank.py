# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class RankRank(models.Model):
    _name = "rank.rank"
    _description = "Rank"

    name = fields.Char()
    description = fields.Text()
    salary_range = fields.Text()
    active = fields.Boolean(default=True)

    _sql_constraints = [("name_uniq", "unique(name)", "Rank should be unique")]

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=80):
        """Search the rank based on grade."""
        if self.env.context.get("grade"):
            grade_rank_recs = (
                self.env["grade.grade"]
                .sudo()
                .search([("id", "=", self.env.context.get("grade"))])
                .mapped("rank_ids")
            )
            args += [("id", "in", grade_rank_recs.ids or [])]
        return super(RankRank, self).name_search(
            name=name, args=args, operator=operator, limit=limit
        )


class GradeGrade(models.Model):
    _name = "grade.grade"
    _description = "Grade"

    name = fields.Char()
    description = fields.Text()
    rank_ids = fields.Many2many(
        "rank.rank", "rel_grade_rank", "grade_id", "rank_id", "Ranks"
    )
    active = fields.Boolean(default=True)


class HrEmployee(models.Model):

    _inherit = "hr.employee"

    grade_id = fields.Many2one("grade.grade", "Grade")
    rank_id = fields.Many2one("rank.rank", "Rank")
