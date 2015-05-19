# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2013 Serpent Consulting Services Pvt. Ltd. (<http://www.serpentcs.com>)
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

from openerp import models, fields, api, _

import time

class base_synchro_server(models.Model):
    '''Class to store the information regarding server'''
    _name = "base.synchro.server"
    _description = "Synchronized server"

    name = fields.Char(string='Server name', size=64, required=True)
    server_url = fields.Char(string='Server URL', size=64, required=True)
    server_port = fields.Integer(string='Server Port', size=64, required=True, default=8069)
    server_db = fields.Char(string='Server Database', size=64, required=True)
    login = fields.Char(string='User Name', size=50, required=True)
    password = fields.Char(string='Password', size=64, required=True)
    obj_ids = fields.One2many('base.synchro.obj', 'server_id', string='Models', ondelete='cascade')

class base_synchro_obj(models.Model):
    '''Class to store the operations done by wizard'''
    _name = "base.synchro.obj"
    _description = "Register Class"
    _order = 'sequence'

    name = fields.Char(string='Name', size=64, select=1, required=1)
    domain = fields.Char(string='Domain', size=64, select=1, required=1,default='[]')
    server_id = fields.Many2one('base.synchro.server', string='Server', ondelete='cascade', select=1, required=1)
    model_id =  fields.Many2one('ir.model', string='Object to synchronize', required=True)
    action = fields.Selection([('d', 'Download'), ('u', 'Upload'), ('b', 'Both')], string='Synchronisation direction', required=True, default='d')
    sequence =  fields.Integer(string='Sequence')
    active =  fields.Boolean(string='Active', default=True)
    synchronize_date = fields.Datetime(string='Latest Synchronization', readonly=True)
    line_id = fields.One2many('base.synchro.obj.line', 'obj_id', string='Ids Affected', ondelete='cascade')
    avoid_ids = fields.One2many('base.synchro.obj.avoid', 'obj_id', string='Fields Not Sync.')

    #
    # Return a list of changes: [ (date, id) ]
    #

    @api.model
    def get_ids(self, object, dt, domain=[], action=None):
        if action is None:
            action = {}
        return self._get_ids(object, dt, domain, action=action)

    @api.model
    def _get_ids(self, object, dt, domain=[], action=None):
        if action is None:
            action = {}
        POOL = self.env[object]
        result = []
        if dt:
            domain2 = domain + [('write_date', '>=', dt)]
            domain3 = domain + [('create_date', '>=', dt)]
        else:
            domain2 = domain3 = domain
        ids = POOL.search(domain2)
        ids += POOL.search(domain3)
        for r in ids.read(['create_date','write_date']):
            result.append((r['write_date'] or r['create_date'], r['id'], action.get('action', 'd')))
        return result

class base_synchro_obj_avoid(models.Model):
    _name = "base.synchro.obj.avoid"
    _description = "Fields to not synchronize"

    name = fields.Char(string='Field Name', size=64, select=1, required=1)
    obj_id = fields.Many2one('base.synchro.obj', 'Object', required=1, ondelete='cascade')

class base_synchro_obj_line(models.Model):
    '''Class to store the operations done by wizard'''
    _name = "base.synchro.obj.line"
    _description = "Synchronized instances"

    name = fields.Datetime('Date', required=True, default=lambda *args: time.strftime('%Y-%m-%d %H:%M:%S'))
    obj_id = fields.Many2one('base.synchro.obj', 'Object', ondelete='cascade', select=True)
    local_id = fields.Integer('Local Id', readonly=True)
    remote_id = fields.Integer('Remote Id', readonly=True)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
