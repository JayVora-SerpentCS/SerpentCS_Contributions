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
            self._cr.execute('select count(id) from crm_lead \
                where stage_id =%s', (stage.id,))
            leads = self._cr.fetchone()
            crm_lst.append((stage.name, int(leads and leads[0])))
        return crm_lst

    @api.multi
    def write(self, vals):
        active = vals.get('active', False)
        ir_model = self.env['ir.model.data']
        stage_id = self.stage_id
        if active:
            stage_id = ir_model.get_object('crm', 'stage_lead1')
        elif not active:
            stage_id = ir_model.get_object('web_lead_funnel_chart',
                                           'stage_lead_archive')
        vals.update({'stage_id': stage_id.id})
        return super(Crmleadextended, self).write(vals)
