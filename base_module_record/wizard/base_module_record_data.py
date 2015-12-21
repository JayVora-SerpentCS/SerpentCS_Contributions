# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time

from openerp.tools import frozendict, ustr
from openerp.tools.translate import _
from openerp import models, fields, api


class base_module_data(models.TransientModel):
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
                                 default=lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'))
    objects = fields.Many2many('ir.model', 'base_module_record_model_rel', 'objects',
                               'model_id', 'Objects', default=_get_default_objects)
    filter_cond = fields.Selection([('created', 'Created'), ('modified', 'Modified'),
                                    ('created_modified', 'Created & Modified')],
                                   'Records only', required=True, default='created')
    info_yaml = fields.Boolean('YAML')

    @api.model
    def _create_xml(self, data):
        mod = self.env['ir.module.record']
        res_xml = mod.generate_xml()
        return {'res_text': res_xml}

    @api.model
    def _create_yaml(self, data):
        mod = self.env['ir.module.record']
        res_xml = mod.generate_yaml()
        return { 'res_text': res_xml}

    @api.multi
    def record_objects(self):
        data = self.read([])[0]
        check_date = data['check_date']
        filter_cond = data['filter_cond']
        mod_obj = self.env['ir.model']
        cr, uid, context = self.env.args
        context = dict(context)
        context.update({'recording_data': []})
        recording_data = context.get('recording_data')
        self.env.args = cr, uid, frozendict(context)
        for id in data['objects']:
            obj_name = (mod_obj.browse(id)).model
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
                args = (dbname, self.env.user.id, obj_name, 'copy', s_id.id, {})
                recording_data.append(('query', args, {}, s_id.id))
        mod_obj = self.env['ir.model.data']
        if len(recording_data):
            if data['info_yaml']:
                res = self._create_yaml(data)
            else:
                res = self._create_xml(data)
            model_data_ids = mod_obj.search([('model', '=', 'ir.ui.view'),
                                             ('name', '=', 'module_create_xml_view')])
            print "model_data_ids::::::::::::::::::",model_data_ids
            resource_id = model_data_ids.read(['res_id'])[0]['res_id']
            return {
                'name': _('Data Recording'),
                'context': {'default_res_text': ustr(res['res_text'])},
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'base.module.record.data',
                'views': [(resource_id, 'form')],
                'type': 'ir.actions.act_window',
                'target': 'new',
            }
        model_data_ids = mod_obj.search([('model', '=', 'ir.ui.view'),
                                         ('name', '=', 'module_recording_message_view')])
        resource_id = model_data_ids.read(['res_id'])[0]['res_id']
        return {
            'name': _('Module Recording'),
            'context': {},
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'base.module.record.objects',
            'views': [(resource_id, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'new',
        }


class base_module_record_data(models.TransientModel):
    _name = "base.module.record.data"
    _description = "Base Module Record Data"

    res_text = fields.Text('Result')
