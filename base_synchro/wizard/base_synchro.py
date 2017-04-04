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

import time
import xmlrpclib
import threading
import logging
from openerp import pooler
from openerp.tools import frozendict
from openerp import models, fields, api
from openerp.osv import osv
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)

class RPCProxyOne(object):
    def __init__(self, server, ressource):
        self.server = server
        local_url = 'http://%s:%d/xmlrpc/common' % (server.server_url, server.server_port)
        rpc = xmlrpclib.ServerProxy(local_url)
        self.uid = rpc.login(server.server_db, server.login, server.password)
        local_url = 'http://%s:%d/xmlrpc/object' % (server.server_url, server.server_port)
        self.rpc = xmlrpclib.ServerProxy(local_url)
        self.ressource = ressource
    def __getattr__(self, name):
#        RPCProxy(self.server)
#        pool1 = RPCProxy(self.server)
#        sync_obj = pool1.get('base.synchro.obj')
#        return self.rpc.execute(self.server.server_db, self.uid, sync_obj, name, (), {})
        return lambda cr, uid, *args, **kwargs: self.rpc.execute(self.server.server_db, self.uid, self.server.password, self.ressource, name, *args)

class RPCProxy(object):
    def __init__(self, server):
        self.server = server

    def get(self, ressource):
        return RPCProxyOne(self.server, ressource)

class base_synchro(models.TransientModel):
    """Base Synchronization """
    _name = 'base.synchro'

    server_url = fields.Many2one('base.synchro.server', "Server URL", required=True)
    user_id = fields.Many2one('res.users', "Send Result To",default=lambda self: self.env.user)

#    start_date = time.strftime('%Y-%m-%d, %Hh %Mm %Ss')
    report = []
    report_total = 0
    report_create = 0
    report_write = 0

    @api.model
    def input(self, ids, value):
#        for key,valu in  zip(value.keys(),value.values()) :
#            if type(valu) is unicode:
#                val=tools.ustr(valu)
#                print "\n\n value",val
#                c=unicodedata.normalize('NFKD', valu).encode('ascii','ignore')#
#                a=valu.encode('utf-8')
#                print "aaaa.=",a
#                value[key]=val
        return value

    @api.model
    def synchronize(self, server, object):
        pool = pooler.get_pool(self.env.cr.dbname)
        self.meta = {}
        ids = []
        pool1 = RPCProxy(server)
        pool2 = pool
#        context = dict(self._context)
        # try:
        if object.action in ('d', 'b'):
            module = pool1.get("ir.module.module")
            module_id  = module.search(self._cr, self.user_id.id, [("name","ilike","base_synchro"), ('state','=','installed')])
            if not module_id:
                raise osv.except_osv(_('Warning'),
                             _('If your Synchronisation direction is download or both, please install \
                             "Multi-DB Synchronization" module in targeted server!'))
            ids = pool1.get('base.synchro.obj').get_ids(self._cr, self.user_id, object.model_id.model, object.synchronize_date, eval(object.domain), {'action':'d'})

        if object.action in ('u', 'b'):
            _logger.debug("Getting ids to synchronize [%s] (%s)", object.synchronize_date, object.domain)
            ids += pool2.get('base.synchro.obj').get_ids(self._cr, self.user_id.id, object.model_id.model, object.synchronize_date, eval(object.domain), {'action':'u'})
        ids.sort()
        iii = 0

        for dt, id, action in ids:
            iii += 1
            if action == 'd':
                pool_src = pool1
                pool_dest = pool2
            else:
                pool_src = pool2
                pool_dest = pool1
            fields = False
            if object.model_id.model == 'crm.case.history':
                fields = ['email', 'description', 'log_id']
            value = pool_src.get(object.model_id.model).read(self._cr, self.user_id.id, [id], fields)[0]
#            value = pool_src.get(object.model_id.model).read([id], fields)[0] 
            if 'create_date' in value:
                del value['create_date']
            if 'write_date' in value:
                del value['write_date']

            # Use val[0] on many2one because it comes like (id, 'name')
            for key , val in value.iteritems():
                if type(val) == tuple:
                    value.update({key:val[0]})
            value = self.data_transform(pool_src, pool_dest, object.model_id.model, value, action)

            # Search if record exists by name in dst
            id_remote = self.get_existing_dst(pool_src, pool_dest, object, id, action)

            # If it exists, create synchro.obj.line record with local and remote ids
            if id_remote:
                # TODO: It is not tested for download or both, only for upload
                self.env['base.synchro.obj.line'].create({
                    'obj_id': object.id,
                    'local_id': id,
                    'remote_id': id_remote,
                })

            # Search id on synchronized objects
            id2 = self.get_id(object.id, id, action)

            if not (iii % 50):
                pass

            # Filter fields to not sync
            for field in object.avoid_ids:
                if field.name in value:
                    del value[field.name]
            if id2:
                # try:
                _logger.debug("Updating model %s [%d]", object.model_id.name, id2)
                pool_dest.get(object.model_id.model).write(self._cr, self.user_id.id, [id2], value)
                # except Exception, e:
                # self.report.append('ERROR: Unable to update record ['+str(id2)+']:'+str(value.get('name', '?')))
                self.report_total += 1
                self.report_write += 1
            else:
#                value_encode = self.input(ids, value)
#                idnew = pool_dest.get(object.model_id.model).create(self._cr, self.user_id.id, value_encode)
                _logger.debug("Creating model %s", object.model_id.name)
                idnew = pool_dest.get(object.model_id.model).create(self._cr, self.user_id.id, value)
                self.env['base.synchro.obj.line'].create({
                    'obj_id': object.id,
                    'local_id': (action == 'u') and id or idnew,
                    'remote_id': (action == 'd') and id or idnew
                })
                self.report_total += 1
                self.report_create += 1
            self.meta = {}
        return True

    @api.model
    def get_id(self, object_id, id, action):
        pool = pooler.get_pool(self.env.cr.dbname)
        line_pool = pool.get('base.synchro.obj.line')
        field_src = (action == 'u') and 'local_id' or 'remote_id'
        field_dest = (action == 'd') and 'local_id' or 'remote_id'
        rid = line_pool.search(self._cr, self.user_id.id, [('obj_id', '=', object_id), (field_src, '=', id)])
        result = False
        if rid:
            result = line_pool.read(self._cr, self.user_id.id, rid, [field_dest])[0][field_dest]
        return result

    @api.model
    def get_existing_dst(self, pool_src, pool_dest, object_to_sync, res_id, action):

        obj_model = object_to_sync.model_id.model
        fields_of_equality = object_to_sync.fields_of_equality.mapped(lambda x: x.name)

        _logger.debug("Searching existing object in dest. %s [%d]", obj_model, res_id)

        # If fields_of_equality are not set, we search by name_search
        if not fields_of_equality:
            # Get local name
            _logger.debug("Searching by name_search")
            names = pool_src.get(obj_model).name_get(self._cr,
                            self.user_id.id, [res_id])[0][1]

            # Search remote by name_search
            res = pool_dest.get(obj_model).name_search(self._cr, self.user_id.id, names, [], 'like')
            if not res:
                return False
            else:
                res = res[0]

        else:
            # Read fields of equality
            _logger.debug("Searching by fields of equality [%s]", fields_of_equality)
            fvalues = pool_src.get(obj_model).read(self._cr, self.user_id.id,
                            res_id, fields_of_equality)

            # We assemble domain to search for equality
            domain = []
            for f, v in fvalues.iteritems():
                if f == 'id':
                    continue

                domain.append((f, '=', v))

            # Search in desitny
            res = pool_dest.get(obj_model).search(self._cr, self.user_id.id, domain)

        if res:
            _logger.debug("Object found in dest with id: %d", res[0])
            return res[0]
        else:
            _logger.debug("Object not found in dest")
            return False

    @api.model
    def relation_transform(self, pool_src, pool_dest, obj_model, res_id, action):
        if not res_id:
            return False
#        pool = pooler.get_pool(self.env.cr.dbname)
        _logger.debug("Relation transform")
        self._cr.execute('''select o.id from base_synchro_obj o left join ir_model m on (o.model_id =m.id) where
                m.model=%s and
                o.active''', (obj_model,))
        obj = self._cr.fetchone()
        result = False
        if obj:
            #
            # If the object is synchronised and found, set it
            #
            result = self.get_id(obj[0], res_id, action)
            _logger.debug("Relation object already synchronized. Getting id...%s", result)
        else:
            #
            # If not synchronized, try to find it with name_get/name_search
            #
            _logger.debug("Relation object not synchronized. Searching by name_get and name_search")
            names = pool_src.get(obj_model).name_get(self._cr, self.user_id.id, [res_id])[0][1]
            _logger.debug("name_get in src: %s", names)
            res = pool_dest.get(obj_model).name_search(self._cr, self.user_id.id, names, [], 'like')
            _logger.debug("name_search in dest: %s", res)
            if res:
                result = res[0][0]
            else:
                # LOG this in the report, better message.
                _logger.warning("Record '%s' on relation %s not found, set to null.", names, obj_model)
                _logger.warning("You should consider synchronize this model '%s'", obj_model)
                self.report.append('WARNING: Record "%s" on relation %s not found, set to null.' % (names, obj_model))
        return result

    #
    # IN: object and ID
    # OUT: ID of the remote object computed:
    #        If object is synchronised, read the sync database
    #        Otherwise, use the name_search method
    #

    @api.model
    def data_transform(self, pool_src, pool_dest, obj, data, action=None):
        if action is None:
            action = {}
#        self.meta.setdefault(pool_src, {})
#        if not obj in self.meta[pool_src]:
        fields = pool_src.get(obj).fields_get(self._cr, self.user_id.id)
#        fields = self.meta[pool_src][obj]
        _logger.debug("Transforming data")
        for f in fields:
            if f not in data:
                continue
            ftype = fields[f]['type']
            if ftype in ('function', 'one2many', 'one2one'):
                _logger.debug("Field %s of type %s, discarded.", f, ftype)
                del data[f]
            elif ftype == 'many2one':
                _logger.debug("Field %s is many2one", f)
                if (isinstance(data[f], list)) and data[f]:
                    fdata = data[f][0]
                else:
                    fdata = data[f]
                # Search relation
                df = self.relation_transform(pool_src, pool_dest, fields[f]['relation'], fdata, action)
                data[f] = df
                if not data[f]:
                    del data[f]
            elif ftype == 'many2many':
                res = map(lambda x: self.relation_transform(pool_src, pool_dest, fields[f]['relation'], x, action), data[f])
                data[f] = [(6, 0, [x for x in res if x])]
        del data['id']
        return data

    #
    # Find all objects that are created or modified after the synchronize_date
    # Synchronize these obejcts
    #

    @api.multi
    def upload_download(self):
        self.report = []
        start_date = time.strftime('%Y-%m-%d, %Hh %Mm %Ss')
        syn_obj = self.browse(self.ids)[0]
#        pool = pooler.get_pool(self.env.cr.dbname)
        server = self.env['base.synchro.server'].browse(syn_obj.server_url.id)
        for obj_rec in server.obj_ids:
            _logger.debug("Start synchro of %s", obj_rec.name)
            dt = time.strftime('%Y-%m-%d %H:%M:%S')
            self.synchronize(server, obj_rec)
            if obj_rec.action == 'b':
                time.sleep(1)
                dt = time.strftime('%Y-%m-%d %H:%M:%S')
            obj_rec.write({'synchronize_date': dt})
        end_date = time.strftime('%Y-%m-%d, %Hh %Mm %Ss')
#        return {}

        # Creating res.request for summary results
        if syn_obj.user_id:
            cr, uid, context = self.env.args
            request = pooler.get_pool(cr.dbname).get('res.request')
            if not self.report:
                self.report.append('No exception.')
            summary = '''Here is the synchronization report:

Synchronization started: %s
Synchronization finnished: %s

Synchronized records: %d
Records updated: %d
Records created: %d

Exceptions:
            ''' % (start_date, end_date, self.report_total, self.report_write, self.report_create)
            summary += '\n'.join(self.report)
            if request:
                request.create(cr, uid, {
                    'name' : "Synchronization report",
                    'act_from' : self.user_id.id,
                    'date': time.strftime('%Y-%m-%d, %H:%M:%S'),
                    'act_to' : syn_obj.user_id.id,
                    'body': summary,
                }, context=context)
            return {}

    @api.multi
    def upload_download_multi_thread(self):
        threaded_synchronization = threading.Thread(target=self.upload_download())
        threaded_synchronization.run()
        data_obj = self.env['ir.model.data']
        id2 = data_obj._get_id('base_synchro', 'view_base_synchro_finish')
        if id2:
            id2 = data_obj.browse(id2).res_id
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'base.synchro',
            'views': [(id2, 'form')],
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
