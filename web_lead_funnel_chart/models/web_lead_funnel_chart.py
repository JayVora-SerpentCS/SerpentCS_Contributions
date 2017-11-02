# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class Crmleadextended(models.Model):
    _inherit = 'crm.lead'

    @api.multi
    def get_lead_stage_data(self):
        self._cr.execute('select id from crm_stage')
        stage_ids = [stage_id[0] for stage_id in self._cr.fetchall()]
        crm_lst = []
        stages = self.env['crm.stage'].browse(stage_ids)
        for stage in stages:
            if stage:
                self._cr.execute('select count(id) from crm_lead \
                where stage_id =%s', (stage.id, ))
                leads = self._cr.fetchone()
                crm_lst.append((stage.name, int(leads and leads[0] or 0)))
        return crm_lst

    #This method is overridden for archiving stage of funnel chart
    @api.multi
    def write(self, vals):
        active = vals.get('active', False)
        ir_model = self.env['ir.model.data']
        stage_id = self.stage_id
        if active:
            stage_id = ir_model.get_object('crm', 'stage_lead1')
        else:
            stage_id = ir_model.get_object('web_lead_funnel_chart',
                                           'stage_lead_archive')
        vals.update({'stage_id': stage_id.id})
        return super(Crmleadextended, self).write(vals)


class StageExtended(models.Model):
    _inherit = 'crm.stage'

    active = fields.Boolean('Active', default=True)
