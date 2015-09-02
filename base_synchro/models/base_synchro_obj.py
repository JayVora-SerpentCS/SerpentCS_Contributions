# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2011-Today Serpent Consulting Services Pvt. Ltd.
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
    obj_ids = fields.One2many('base.synchro.obj', 'server_id',
                              string='Models', ondelete='cascade')


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
    action = fields.Selection([('d', 'Download'),
                               ('u', 'Upload'),
                               ('b', 'Both')],
                              'Synchronisation direction',
                              required=True, default='d')
    sequence = fields.Integer('Sequence')
    active = fields.Boolean('Active', default=True)
    synchronize_date = fields.Datetime('Latest Synchronization', readonly=True)
    line_id = fields.One2many('base.synchro.obj.line', 'obj_id',
                              'IDs Affected', ondelete='cascade')
    avoid_ids = fields.One2many('base.synchro.obj.avoid', 'obj_id',
                                'Fields Not Sync.')

    #
    # Return a list of changes: [ (date, id) ]
    #

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
            result.append((r['write_date'] or r['create_date'], r['id'],
                           action.get('action', 'd')))
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

    current_time = lambda *args: time.strftime('%Y-%m-%d %H:%M:%S')
    name = fields.Datetime('Date', required=True,
                           default=current_time)
    obj_id = fields.Many2one('base.synchro.obj', 'Object', ondelete='cascade',
                             select=1)
    local_id = fields.Integer('Local ID', readonly=True)
    remote_id = fields.Integer('Remote ID', readonly=True)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
