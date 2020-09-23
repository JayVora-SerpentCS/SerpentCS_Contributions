# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    member_ids = fields.Many2many('res.users', 'project_user_rel', 'project_id',
                                  'uid', 'Project Members', help="""Project's
                               members are users who can have an access to
                               the tasks related to this project."""
                                  )
    team_id = fields.Many2one('crm.team', "Project Team",
                              domain=[('type_team', '=', 'project')])

    @api.onchange('team_id')
    def _get_team_members(self):
        self.update({"member_ids": [(6, 0,
                                    self.team_id.team_member_ids.ids)]})
