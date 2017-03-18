# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
from odoo import api, models


class Crmleadextended(models.Model):
    _inherit = 'crm.lead'

    @api.multi
    def get_lead_stage_data(self):
        stage_ids = self.env['crm.stage'].search([])
        crm_lst = []
        for stage in stage_ids:
            self._cr.execute(
                '''select count(*) from crm_lead where stage_id=%s'''
                % stage.id)
            leads = self._cr.fetchone()
            crm_lst.append((stage.name, int(leads[0])))
        return crm_lst
