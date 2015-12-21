# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time
import base_module_save

from openerp.tools import frozendict, ustr
from openerp.tools.translate import _
from openerp import models, fields, api


class base_module_record(models.TransientModel):
    _name = 'base.module.record'
    _description = "Base Module Record"

    @api.model
    def _get_default_objects(self):
        names = ('ir.ui.view', 'ir.ui.menu', 'ir.model',
                 'ir.model.fields', 'ir.model.access',
                 'res.partner', 'res.partner.address',
                 'res.partner.category', 'workflow',
                 'workflow.activity', 'workflow.transition',
                 'ir.actions.server', 'ir.server.object.lines')
        return self.env['ir.model'].search([('model', 'in', names)])

    check_date = fields.Datetime('Record from Date', required=True,
                                 default=lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'))
    objects = fields.Many2many('ir.model', 'base_module_record_object_rel', 'objects',
                               'model_id', 'Objects', default=_get_default_objects)
    filter_cond =  fields.Selection([('created', 'Created'),
                                     ('modified', 'Modified'),
                                     ('created_modified', 'Created & Modified')],
                                    'Records only', required=True, default='created')
    info_yaml = fields.Boolean('YAML')

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
        for obj_id in data['objects']:
            obj_name = (mod_obj.browse(obj_id)).model
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
                res = base_module_save._create_yaml(self, data)
                model_data_ids = mod_obj.search([('model', '=', 'ir.ui.view'),
                                                 ('name', '=', 'yml_save_form_view')])
                resource_id = model_data_ids.read(['res_id'])[0]['res_id']
                return {
                    'name': _('Module Recording'),
                    'context': {
                        'default_yaml_file': ustr(res['yaml_file']),
                        'default_module_filename': 'demo_yaml.yml',
                    },
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'base.module.record.objects',
                    'views': [(resource_id, 'form')],
                    'type': 'ir.actions.act_window',
                    'target': 'new',
                }
            else:
                model_data_ids = mod_obj.search([('model', '=', 'ir.ui.view'),
                                                 ('name', '=', 'info_start_form_view')])
                resource_id = model_data_ids.read(['res_id'])[0]['res_id']
                return {
                    'name': _('Module Recording'),
                    'context': context,
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'base.module.record.objects',
                    'views': [(resource_id, 'form')],
                    'type': 'ir.actions.act_window',
                    'target': 'new',
                }
        model_data_ids = mod_obj.search([('model', '=', 'ir.ui.view'),
                                         ('name', '=', 'module_recording_message_view')])
        resource_id = model_data_ids.read(['res_id'])[0]['res_id']
        return {
            'name': _('Module Recording'),
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'base.module.record.objects',
            'views': [(resource_id, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'new',
        }


class base_module_record_objects(models.TransientModel):
    _name = 'base.module.record.objects'
    _description = "Base Module Record Objects"

    @api.model
    def inter_call(self, data):
        cr, uid, context = self.env.args
        context = dict(context)
        context.update({'depends': {}})
        self.env.args = cr, uid, frozendict(context)
        res = base_module_save._create_module(self, self._cr, self.env.user.id,
                                              data, context=context)
        mod_obj = self.env['ir.model.data']
        model_data_ids = mod_obj.search([('model', '=', 'ir.ui.view'),
                                         ('name', '=', 'module_create_form_view')])
        resource_id = model_data_ids.read(fields=['res_id'])[0]['res_id']
        context.update(res)
        module_rec = self.env['base.module.record.objects'].create({
                     'module_filename': ustr(res['module_filename']),
                     'module_file': ustr(res['module_file'])})
        return {
            'name': _('Module Recording'),
            'res_id' : module_rec.id,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'base.module.record.objects',
            'views': [(resource_id, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    name = fields.Char('Module Name', size=64 )
    directory_name = fields.Char('Directory Name', size=32 )
    version = fields.Char('Version', size=16 )
    author = fields.Char('Author', size=64, required=True, default='OpenERP SA')
    category =  fields.Char('Category', size=64, required=True,
                            default='Vertical Modules/Parametrization')
    website = fields.Char('Documentation URL', size=64, required=True,
                          default='http://www.openerp.com')
    description = fields.Text('Full Description')
    data_kind =  fields.Selection([('demo', 'Demo Data'),('update', 'Normal Data')],
                                  'Type of Data', required=True, default='update')
    module_file = fields.Binary('Module .zip File', filename="module_filename")
    module_filename = fields.Char('Filename', size=64)
    yaml_file = fields.Binary('Module .zip File')
