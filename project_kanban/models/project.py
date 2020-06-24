# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Project(models.Model):
    _inherit = "project.project"

    @api.depends("message_ids")
    def _compute_get_recent_date(self):
        for project in self:
            date_lst = [x.date for x in project.message_ids]
            project.recent_date = date_lst and max(date_lst) or False

    recent_date = fields.Datetime(
        compute="_compute_get_recent_date",
        string="Recent date",
        help="This will be auto set",
    )


class ProjectTask(models.Model):
    _inherit = "project.task"

    def write(self, vals):
        res = super(ProjectTask, self).write(vals)
        self.project_id.write_date = self.write_date
        return res
