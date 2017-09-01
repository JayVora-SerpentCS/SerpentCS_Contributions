# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time
from openerp import models, fields, api


class base_synchro_server(models.Model):
    '''Class to store the information regarding server'''
    _name = "base.synchro.server"
    _description = "Synchronized server"

    name = fields.Char('Server name', required=True)
    server_url = fields.Char('Server URL', required=True)
    server_port = fields.Integer('Server Port', required=True, default=8069)
    server_db = fields.Char('Server Database', required=True)
    login = fields.Char('User Name', required=True)
    password = fields.Char('Password', required=True)
    obj_ids = fields.One2many('base.synchro.obj', 'server_id', string='Models',
                              ondelete='cascade')


class base_synchro_obj(models.Model):
    '''Class to store the operations done by wizard'''
    _name = "base.synchro.obj"
    _description = "Register Class"
    _order = 'sequence'

    name = fields.Char('Name', select=1, required=True)
    domain = fields.Char('Domain', select=1, required=True, default='[]')
    server_id = fields.Many2one('base.synchro.server', 'Server',
                                ondelete='cascade', select=1, required=True)
    model_id = fields.Many2one('ir.model', string='Object to synchronize',
                               required=True)
    action = fields.Selection([('d', 'Download'), ('u', 'Upload'),
                               ('b', 'Both')], 'Synchronisation direction',
                              required=True, default='d')
    sequence = fields.Integer('Sequence')
    active = fields.Boolean('Active', default=True)
    synchronize_date = fields.Datetime('Latest Synchronization', readonly=True)
    line_id = fields.One2many('base.synchro.obj.line', 'obj_id',
                              'IDs Affected', ondelete='cascade')
    avoid_ids = fields.One2many('base.synchro.obj.avoid', 'obj_id',
                                'Fields Not Sync.')

    @api.model
    def get_ids(self, obj, dt, domain=[], action=None):
        if action is None:
            action = {}
        return self._get_ids(obj, dt, domain, action=action)

    @api.model
    def _get_ids(self, obj, dt, domain=[], action=None):
        if action is None:
            action = {}
        POOL = self.env[obj]
        result = []
        if dt:
            domain2 = domain + [('write_date', '>=', dt)]
            domain3 = domain + [('create_date', '>=', dt)]
        else:
            domain2 = domain3 = domain
        obj_rec = POOL.search(domain2)
        obj_rec += POOL.search(domain3)
        for r in obj_rec.read(['create_date', 'write_date']):
            result.append((r['write_date'] or r['create_date'],
                           r['id'], action.get('action', 'd')))
        return result


class base_synchro_obj_avoid(models.Model):
    _name = "base.synchro.obj.avoid"
    _description = "Fields to not synchronize"

    name = fields.Char('Field Name', select=1, required=True)
    obj_id = fields.Many2one('base.synchro.obj', 'Object',
                             required=True, ondelete='cascade')


class base_synchro_obj_line(models.Model):
    '''Class to store the operations done by wizard'''
    _name = "base.synchro.obj.line"
    _description = "Synchronized instances"

    name = fields.Datetime('Date', required=True, default=lambda *args:
                           time.strftime('%Y-%m-%d %H:%M:%S'))
    obj_id = fields.Many2one('base.synchro.obj', 'Object',
                             ondelete='cascade', select=1)
    local_id = fields.Integer('Local ID', readonly=True)
    remote_id = fields.Integer('Remote ID', readonly=True)
