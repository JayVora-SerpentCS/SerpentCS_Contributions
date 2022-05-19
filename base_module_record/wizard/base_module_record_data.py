# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tools import ustr
from odoo import api, fields, models, _


class BaseModuleData(models.TransientModel):
    _name = "base.module.data"
    _description = "Base Module Data"

    @api.model
    def _get_default_objects(self):
        names = ('ir.ui.view', 'ir.ui.menu', 'ir.model', 'ir.model.fields',
                 'ir.model.access', 'res.partner', 'res.partner.category',
                 'workflow', 'workflow.activity', 'workflow.transition',
                 'ir.actions.server', 'ir.server.object.lines')
        return self.env['ir.model'].search([('model', 'in', names)])

    check_date = fields.Datetime('Record from Date', required=True,
                                 default=fields.Datetime.now)
    objects = fields.Many2many('ir.model', 'base_module_record_model_rel',
                               'objects',
                               'model_id', 'Objects',
                               default=_get_default_objects)
    filter_cond = fields.Selection([('created', 'Created'),
                                    ('modified', 'Modified'),
                                    ('created_modified', 'Created & Modified')
                                    ], 'Records only',
                                   required=True, default='created')

    @api.model
    def _create_xml(self, data):
        res_xml = self.env['ir.module.record'].generate_xml()
        return {'res_text': res_xml}

    @api.multi
    def record_objects(self):
        data = self.read([])[0]
        check_date = data['check_date']
        filter_cond = data['filter_cond']
        mod_obj = self.env['ir.model']
        recording_data = []
        self = self.with_context({'recording_data': recording_data})
        for o_id in data['objects']:
            obj_name = (mod_obj.browse(o_id)).model
            obj_pool = self.env[obj_name]
            if filter_cond == 'created':
                search_condition = [('create_date', '>', check_date)]
            elif filter_cond == 'modified':
                search_condition = [('write_date', '>', check_date)]
            elif filter_cond == 'created_modified':
                search_condition = ['|', ('create_date', '>', check_date),
                                    ('write_date', '>', check_date)]
            if '_log_access' in dir(obj_pool):
                if not (obj_pool._log_access):
                    search_condition = []
                if '_auto' in dir(obj_pool):
                    if not obj_pool._auto:
                        continue
            search_ids = obj_pool.search(search_condition)
            for s_id in search_ids:
                dbname = self.env.cr.dbname
                args = (dbname, self.env.user.id, obj_name,
                        'copy', s_id.id, {})
                recording_data.append(('query', args, {}, s_id.id))
        if len(recording_data):
            res = self._create_xml(data)
            res_id = self.env.ref(
                'base_module_record.module_create_xml_view').id
            return {
                'name': _('Data Recording'),
                'context': {'default_res_text': ustr(res['res_text'])},
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'base.module.record.data',
                'views': [(res_id, 'form')],
                'type': 'ir.actions.act_window',
                'target': 'new',
            }
        res_id = self.env.ref(
            'base_module_record.module_recording_message_view').id
        return {
            'name': _('Module Recording'),
            'context': {},
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'base.module.record.objects',
            'views': [(res_id, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'new',
        }


class BaseModuleRecordData(models.TransientModel):
    _name = "base.module.record.data"
    _description = "Base Module Record Data"

    res_text = fields.Text('Result')
