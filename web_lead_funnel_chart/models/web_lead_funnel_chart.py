# See LICENSE file for full copyright and licensing details.

from odoo import api, models


class Lead(models.Model):
    _inherit = 'crm.lead'

    @api.multi
    def get_lead_stage_data(self):
        stage_ids = self.env['crm.stage'].search([])
        crm_lst = []
        for stage in stage_ids:
            leads = self.search_count([('stage_id', '=', stage.id)])
            crm_lst.append((stage.name, int(leads)))
        return crm_lst
