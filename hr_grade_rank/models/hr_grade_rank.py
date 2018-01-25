# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class RankRank(models.Model):
    _name = 'rank.rank'

    name = fields.Char('Name')
    description = fields.Text('Description')
    salary_range = fields.Text('Salary Range')
    grade_id = fields.Many2one('grade.grade', 'Grade')


class GradeGrade(models.Model):
    _name = 'grade.grade'

    name = fields.Char('Name')
    description = fields.Text('Description')
    rank_ids = fields.One2many('rank.rank', 'grade_id', 'Ranks')


class HrEmployee(models.Model):

    _inherit = 'hr.employee'

    grade_id = fields.Many2one('grade.grade', 'Grade')
    rank_id = fields.Many2one('rank.rank', 'Rank')
