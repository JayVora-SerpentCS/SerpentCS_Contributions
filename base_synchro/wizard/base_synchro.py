# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# 1: imports of python lib
import time
import xmlrpclib
import threading

# 2:  imports of openerp
from openerp import pooler
from openerp import models, fields, api


class RPCProxyOne(object):

    def __init__(self, server, ressource):
        self.server = server
        local_url = 'http://%s:%d/xmlrpc/common' % (server.server_url,
                                                    server.server_port)
        rpc = xmlrpclib.ServerProxy(local_url)
        self.uid = rpc.login(server.server_db, server.login,
                             server.password)
        local_url = 'http://%s:%d/xmlrpc/object' % (server.server_url,
                                                    server.server_port)
        self.rpc = xmlrpclib.ServerProxy(local_url)
        self.ressource = ressource

    def __getattr__(self, name):
        RPCProxy(self.server)
        return lambda cr, uid, *args, **kwargs: self.rpc.execute(
                self.server.server_db,
                self.uid,
                self.server.password,
                self.ressource, name, *args)


class RPCProxy(object):

    def __init__(self, server):
        self.server = server

    def get(self, ressource):
        return RPCProxyOne(self.server, ressource)


class base_synchro(models.TransientModel):
    """Base Synchronization """
    _name = 'base.synchro'

    server_url = fields.Many2one('base.synchro.server', "Server URL",
                                 required=True)
    user_id = fields.Many2one('res.users', "Send Result To",
                              default=lambda self: self.env.user)
    report = []
    report_total = 0
    report_create = 0
    report_write = 0

    @api.model
    def input(self, ids, value):
        return value

    @api.model
    def synchronize(self, server, object):
        pool = pooler.get_pool(self.env.cr.dbname)
        self.meta = {}
        ids = []
        pool1 = RPCProxy(server)
        pool2 = pool
        if object.action in ('d', 'b'):
            ids = pool1.get('base.synchro.obj').get_ids(
                self._cr, self.user_id,
                object.model_id.model,
                object.synchronize_date,
                eval(object.domain),
                {'action': 'd'})

        if object.action in ('u', 'b'):
            ids += pool2.get('base.synchro.obj').get_ids(
                self._cr, self.user_id.id,
                object.model_id.model,
                object.synchronize_date,
                eval(object.domain),
                {'action': 'u'})
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
            value = pool_src.get(object.model_id.model).read(self._cr,
                                                             self.user_id.id,
                                                             [id], fields)[0]
            if 'create_date' in value:
                del value['create_date']
            if 'write_date' in value:
                del value['write_date']
            for key, val in value.iteritems():
                if type(val) == tuple:
                    value.update({key: val[0]})
            value = self.data_transform(pool_src, pool_dest,
                                        object.model_id.model,
                                        value, action)
            id2 = self.get_id(object.id, id, action)
            #
            # Transform value
            #
            if not (iii % 50):
                pass
            # Filter fields to not sync
            for field in object.avoid_ids:
                if field.name in value:
                    del value[field.name]
            if id2:
                pool_dest.get(object.model_id.model).write(self._cr,
                                                           self.user_id.id,
                                                           [id2], value)
                self.report_total += 1
                self.report_write += 1
            else:
                idnew = pool_dest.get(object.model_id.model).create(
                    self._cr,
                    self.user_id.id,
                    value)
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
        rid = line_pool.search(self._cr, self.user_id.id,
                               [('obj_id', '=', object_id),
                                (field_src, '=', id)])
        result = False
        if rid:
            result = line_pool.read(self._cr, self.user_id.id, rid,
                                    [field_dest])[0][field_dest]
        return result

    @api.model
    def relation_transform(self, pool_src, pool_dest, obj_model,
                           res_id, action):
        if not res_id:
            return False
        self._cr.execute('''select o.id from base_synchro_obj o
        left join ir_model m on (o.model_id =m.id) where
         m.model=%s and
         o.active''', (obj_model,))
        obj = self._cr.fetchone()
        result = False
        if obj:
            #
            # If the object is synchronised and found, set it
            #
            result = self.get_id(obj[0], res_id, action)
        else:
            #
            # If not synchronized, try to find it with name_get/name_search
            #
            names = pool_src.get(obj_model).name_get(self._cr,
                                                     self.user_id.id,
                                                     [res_id])[0][1]
            res = pool_dest.get(obj_model).name_search(self._cr,
                                                       self.user_id.id,
                                                       names, [], 'like')
            if res:
                result = res[0][0]
            else:
                # LOG this in the report, better message.
                print self.report.append('''WARNING: Record "%s" on
                relation %s not found, set to null.''' % (names, obj_model))
        return result

    #
    # IN: object and ID
    # OUT: ID of the remote object computed:
    # If object is synchronised, read the sync database Otherwise,
    # use the name_search method
    #

    @api.model
    def data_transform(self, pool_src, pool_dest, obj, data, action=None):
        if action is None:
            action = {}
        fields = pool_src.get(obj).fields_get(self._cr, self.user_id.id)
        for f in fields:
            if f not in data:
                continue
            ftype = fields[f]['type']
            if ftype in ('function', 'one2many', 'one2one'):
                del data[f]
            elif ftype == 'many2one':
                if (isinstance(data[f], list)) and data[f]:
                    fdata = data[f][0]
                else:
                    fdata = data[f]
                df = self.relation_transform(pool_src, pool_dest,
                                             fields[f]['relation'],
                                             fdata, action)
                data[f] = df
                if not data[f]:
                    del data[f]
            elif ftype == 'many2many':
                res = map(lambda x: self.relation_transform(
                    pool_src, pool_dest,
                    fields[f]['relation'],
                    x, action), data[f])
                data[f] = [(6, 0, [x for x in res if x])]
        del data['id']
        return data

    #
    # Find all objects that are created or modified after the synchronize_date
    # Synchronize these obejcts
    #

    @api.multi
    def upload_download(self):
        start_date = time.strftime('%Y-%m-%d, %Hh %Mm %Ss')
        syn_obj = self.browse(self.ids)[0]
#        pool = pooler.get_pool(self.env.cr.dbname)
        server = self.env['base.synchro.server'].browse(syn_obj.server_url.id)
        for obj_rec in server.obj_ids:
            dt = time.strftime('%Y-%m-%d %H:%M:%S')
            self.synchronize(server, obj_rec)
            if obj_rec.action == 'b':
                time.sleep(1)
                dt = time.strftime('%Y-%m-%d %H:%M:%S')
            self.env['base.synchro.obj'].write({'synchronize_date': dt})
        end_date = time.strftime('%Y-%m-%d, %Hh %Mm %Ss')
#        return {}
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
            ''' % (start_date, end_date, self.report_total,
                   self.report_write, self.report_create)
            summary += '\n'.join(self.report)
            if request:
                request.create(cr, uid, {
                    'name': "Synchronization report",
                    'act_from': self.user_id.id,
                    'date': time.strftime('%Y-%m-%d, %H:%M:%S'),
                    'act_to': syn_obj.user_id.id,
                    'body': summary,
                }, context=context)
            return {}

    @api.multi
    def upload_download_multi_thread(self):
        threaded_synchronization = \
            threading.Thread(target=self.upload_download())
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
