# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class CrmTeamInherit(models.Model):
    _inherit = 'crm.team'

    type_team = fields.Selection([('sale', 'Sale'), ('project', 'Project')],
                                 "Type", default="sale")
    team_members = fields.Many2many('res.users', 'project_team_user_rel',
                                    'team_id', 'uid', 'Project Members',
                                    help="""Project's members are users who
                                     can have an access to the tasks related
                                     to this project.""")
