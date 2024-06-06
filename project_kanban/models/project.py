from odoo import api, fields, models

class Project(models.Model):
    _inherit = "project.project"

    @api.depends("task_ids.write_date")
    def _compute_get_recent_date(self):
        for project in self:
            recent_date = max(task.write_date for task in project.task_ids) if project.task_ids else False
            project.recent_date = recent_date

    recent_date = fields.Datetime(
        compute="_compute_get_recent_date",
        string="Recent date",
        help="This will be automatically set by changing in any task of this project.",
    )

class ProjectTask(models.Model):
    _inherit = "project.task"

    def write(self, vals):
        """This method used for changing project write date."""
        res = super(ProjectTask, self).write(vals)
        if 'write_date' in vals:
            self.project_id.write_date = max(task.write_date for task in self.project_id.task_ids)
        return res
