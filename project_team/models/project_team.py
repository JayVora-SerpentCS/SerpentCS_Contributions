# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-Today Serpent Consulting Services Pvt. Ltd. (<http://www.serpentcs.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

from openerp import models, fields, api, _

class crm_case_section(models.Model):
    
    _inherit = 'crm.case.section'
    
    type_team = fields.Selection([('sale', 'Sale'), ('project', 'Project')], string="Type", default="sale")


class project_project(models.Model):
    
    _inherit = 'project.project'
    
    team_id = fields.Many2one('crm.case.section', string="Project Team", domain=[('type_team', '=', 'project')])
    
    @api.onchange('team_id')
    def get_team_members(self):
        self.members = [rec.id for rec in self.team_id.member_ids]
        
