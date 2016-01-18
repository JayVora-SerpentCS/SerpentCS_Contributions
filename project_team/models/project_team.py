# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import models, fields, api, _


class CrmTeamInherit(models.Model):

    _inherit = 'crm.team'

    type_team = fields.Selection([('sale', 'Sale'), ('project', 'Project')],
                                 string="Type", default="sale")

    team_members = fields.Many2many('res.users', 'project_team_user_rel',
                                    'team_id','uid', 'Project Members',
                                    help="""Project's members are users who
                                     can have an access to the tasks related
                                     to this project.""")


class ProjectProject(models.Model):

    _inherit = 'project.project'

    members = fields.Many2many('res.users', 'project_user_rel', 'project_id',
                               'uid', 'Project Members', help="""Project's
                               members are users who can have an access to
                               the tasks related to this project.""",
                               states={'close':[('readonly',True)],
                                       'cancelled':[('readonly',True)]})
    team_id = fields.Many2one('crm.team', string="Project Team",
                              domain=[('type_team', '=', 'project')])

    @api.onchange('team_id')
    def get_team_members(self):
        self.members = [(6,0,[rec.id for rec in self.team_id.team_members])]
