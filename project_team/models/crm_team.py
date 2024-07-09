# See LICENSE file for full copyright and licensing details.

import ast
from odoo import fields, models, api


class CrmTeamInherit(models.Model):
    _inherit = 'crm.team'

    type_team = fields.Selection([('sale', 'Sale'), ('project', 'Project')],
                                 string="Team Type", default="sale")
    team_members_ids = fields.Many2many('res.users', 'project_team_user_rel',
                                        'team_id', 'user_id', 'Project Members',
                                        help="""Project's members are users who
                                     can have an access to the tasks related
                                     to this project.""")

class IrModule(models.Model):
    _inherit = "ir.module.module"

    def remove_action(self, action_data):
        domain_lst = ast.literal_eval(action_data.domain)
        return [domain for domain in domain_lst if domain[0] != 'type_team']
    
    def module_uninstall(self):
        action_references = [
            'sales_team.crm_team_action_sales',
            'sales_team.crm_team_action_config'
        ]
        
        for ref in action_references:
            action_data = self.env.ref(ref)
            if action_data and action_data.domain:
                action_data.write({'domain': self.remove_action(action_data)})
    
        return super().module_uninstall()
        
