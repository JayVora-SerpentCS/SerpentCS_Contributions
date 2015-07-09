# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-Today Serpent Consulting Services Pvt. Ltd.
#    (<http://www.serpentcs.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from . import base_module_save
from openerp.tools.translate import _
from openerp import models, fields, api
from openerp.tools import frozendict, ustr


class base_module_record(models.TransientModel):
    _name = 'base.module.record'
    _description = "Base Module Record"

    @api.model
    def _get_default_objects(self):
        names = (
            'ir.ui.view', 'ir.ui.menu', 'ir.model', 'ir.model.fields',
            'ir.model.access', 'res.partner', 'res.partner.address',
            'res.partner.category', 'workflow', 'workflow.activity',
            'workflow.transition', 'ir.actions.server',
            'ir.server.object.lines',
        )
        return self.env['ir.model'].search([('model', 'in', names)])

    check_date = fields.Datetime('Record from Date', required=True,
                                 default=lambda *a:
                                 time.strftime('%Y-%m-%d %H:%M:%S'))
    objects = fields.Many2many('ir.model', 'base_module_record_object_rel',
                               'objects', 'model_id', 'Objects',
                               default=_get_default_objects)
    filter_cond = fields.Selection([('created', 'Created'),
                                    ('modified', 'Modified'),
                                    ('created_modified',
                                     'Created & Modified')],
                                   'Records only', required=True,
                                   default='created')
    info_yaml = fields.Boolean('YAML')

    @api.multi
    def record_objects(self):
        data = self.read([])[0]
        check_date = data['check_date']
        filter_cond = data['filter_cond']
#        user = (self.env['res.users'].browse(self.env.user.id)).login
#        mod = self.env['ir.module.record']
        mod_obj = self.env['ir.model']
#        mod.recording_data = []
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
                args = (dbname, self.env.user.id, obj_name, 'copy',
                        s_id.id, {})
                recording_data.append(('query', args, {}, s_id.id))
        mod_obj = self.env['ir.model.data']
        if len(recording_data):
            if data['info_yaml']:
                res = base_module_save._create_yaml(self, data)
                model_data_ids = mod_obj.search([('model', '=', 'ir.ui.view'),
                                                 ('name', '=',
                                                  'yml_save_form_view')])
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
                                                 ('name', '=',
                                                  'info_start_form_view')])
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
                                         ('name', '=',
                                          'module_recording_message_view')])
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
        res = base_module_save._create_module(self, self._cr,
                                              self.env.user.id, data,
                                              context=context)
        mod_obj = self.env['ir.model.data']
        model_data_ids = mod_obj.search([('model', '=', 'ir.ui.view'),
                                         ('name', '=',
                                          'module_create_form_view')])
        resource_id = model_data_ids.read(fields=['res_id'])[0]['res_id']
        context.update(res)
        return {
            'name': _('Module Recording'),
            'context': {
                'default_module_filename': ustr(res['module_filename']),
                'default_module_file': ustr(res['module_file']),
            },
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'base.module.record.objects',
            'views': [(resource_id, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    name = fields.Char('Module Name', size=64, required=True)
    directory_name = fields.Char('Directory Name', size=32, required=True)
    version = fields.Char('Version', size=16, required=True)
    author = fields.Char('Author', size=64, required=True,
                         default='OpenERP SA')
    category = fields.Char('Category', size=64, required=True,
                           default='Vertical Modules/Parametrization')
    website = fields.Char('Documentation URL', size=64, required=True,
                          default='http://www.openerp.com')
    description = fields.Text('Full Description', required=True)
    data_kind = fields.Selection([('demo', 'Demo Data'),
                                  ('update', 'Normal Data')],
                                 'Type of Data',
                                 required=True, default='update')
    module_file = fields.Binary('Module .zip File', filename="module_filename")
    module_filename = fields.Char('Filename', size=64)
    yaml_file = fields.Binary('Module .zip File')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
