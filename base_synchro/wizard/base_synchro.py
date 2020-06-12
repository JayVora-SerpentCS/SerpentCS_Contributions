# See LICENSE file for full copyright and licensing details.

import logging
import time
import threading
from xmlrpc.client import ServerProxy

from odoo import api, fields, models, _
from odoo.exceptions import Warning

_logger = logging.getLogger(__name__)


class RPCProxyOne(object):

    def __init__(self, server, ressource):
        """Class to store one RPC proxy server."""
        self.server = server
        local_url = 'http://%s:%d/xmlrpc/common' % (server.server_url,
                                                    server.server_port)
        try:
            rpc = ServerProxy(local_url, allow_none=True)
            self.uid = rpc.login(server.server_db, server.login,
                                 server.password)
        except Exception as e:
            raise Warning(_(e))
        local_url = 'http://%s:%d/xmlrpc/object' % (server.server_url,
                                                    server.server_port)
        self.rpc = ServerProxy(local_url, allow_none=True)
        self.ressource = ressource

    def __getattr__(self, name):
        return lambda *args: self.rpc.execute(
            self.server.server_db, self.uid, self.server.password,
            self.ressource, name, *args)


class RPCProxy(object):

    def __init__(self, server):
        self.server = server

    def get(self, ressource):
        return RPCProxyOne(self.server, ressource)


class BaseSynchro(models.TransientModel):
    _name = 'base.synchro'
    _description = 'Base Synchronization'

    server_url = fields.Many2one('base.synchro.server', "Server URL",
                                 required=True)
    user_id = fields.Many2one('res.users', "Send Result To",
                              default=lambda self: self.env.user)
    report = []
    report_total = 0
    report_create = 0
    report_write = 0

    @api.model
    def synchronize(self, server, object):
        sync_ids = []
        pool1 = RPCProxy(server)
        pool2 = self
        dt = object.synchronize_date
        module = pool1.get('ir.module.module')
        model_obj = object.model_id.model
        avoid_field_list = [a.name for a in object.avoid_ids]

        if module.search_count([("name", "ilike", "base_synchro"),
                                ('state', '=', 'installed')]) < 1:
            raise Warning(_('If your Synchronization direction is \
                          download and/or upload, please install \
                          "Multi-DB Synchronization" module in targeted \
                          server!'))
        if object.action in ('d', 'b'):
            sync_ids = pool1.get('base.synchro.obj').get_ids(
                model_obj, dt, eval(object.domain), {'action': 'd'})
        if object.action in ('u', 'b'):
            _logger.debug("Getting ids to synchronize [%s] (%s)",
                          object.synchronize_date, object.domain)

            sync_ids += pool2.env['base.synchro.obj'].get_ids(
                model_obj, dt, eval(object.domain), {'action': 'u'})
        for dt, sync_id, action in sync_ids:
            destination_inverted = False
            if action == 'd':
                pool_src = pool1
                pool_dest = pool2
            else:
                pool_src = pool2
                pool_dest = pool1
                destination_inverted = True
            if not destination_inverted:
                value = pool_src.get(object.model_id.model).search_read(
                    [('id', '=', sync_id)])[0]
            else:
                pool = pool_src.env[object.model_id.model]
                value = pool.search_read([('id', '=', sync_id)])[0]
            avoid_field_list += ['create_date', 'write_date']

            field_vals = dict([(key, val[0] if isinstance(val, tuple)
                                else val) for key, val in filter(
                lambda i: i[0] not in avoid_field_list, value.items())])

            value = self.data_transform(
                pool_src, pool_dest, object.model_id.model, field_vals, action,
                destination_inverted, avoid_field_list)
            id2 = self.get_id(object.id, sync_id, action)
            if id2:
                _logger.debug("Updating model %s [%d]", object.model_id.name,
                              id2)
                if not destination_inverted:
                    pool = pool_dest.env[object.model_id.model]
                    pool.browse([id2]).update(value)
                else:
                    pool_dest.get(object.model_id.model).write(id2, value)
                self.report_total += 1
                self.report_write += 1
            else:
                _logger.debug("Creating model %s", object.model_id.name)
                try:
                    if not destination_inverted:
                        new_id = pool_dest.env[object.model_id.model
                                               ].create(value).id
                    else:
                        new_id = pool_dest.get(
                            object.model_id.model).create(value)
                except Exception as e:
                    raise Warning(_(e))
                self.env['base.synchro.obj.line'].create({
                    'obj_id': object.id,
                    'local_id': (action == 'u') and sync_id or new_id,
                    'remote_id': (action == 'd') and sync_id or new_id
                })
                self.report_total += 1
                self.report_create += 1
        return True

    @api.model
    def get_id(self, object_id, id, action):
        synch_line_obj = self.env['base.synchro.obj.line']
        field_src = (action == 'u') and 'local_id' or 'remote_id'
        field_dest = (action == 'd') and 'local_id' or 'remote_id'
        synch_line_rec = synch_line_obj.search_read(
            [('obj_id', '=', object_id), (field_src, '=', id)], [field_dest])
        return synch_line_rec and synch_line_rec[0][field_dest] or False

    @api.model
    def relation_transform(self, pool_src, pool_dest, obj_model, res_id,
                           action, destination_inverted):
        if not res_id:
            return False
        _logger.debug("Relation transform")
        self._cr.execute('''select o.id from base_synchro_obj o left join
                        ir_model m on (o.model_id =m.id) where
                        m.model=%s and o.active''', (obj_model,))
        obj = self._cr.fetchone()
        result = False
        if obj:
            result = self.get_id(obj[0], res_id, action)
            _logger.debug(
                "Relation object already synchronized. Getting id %s",
                result)
        else:
            _logger.debug('Relation object not synchronized. Searching \
             by name_get and name_search')
            if not destination_inverted:
                names = pool_src.get(obj_model).name_get([res_id])[0][1]
                res = pool_dest.env[obj_model].name_search(
                    names, [], 'like', 1)
                res = res and res[0][0] or False
            else:
                pool = pool_src.env[obj_model]
                names = pool.browse([res_id]).name_get()[0][1]
                try:
                    rec_name = pool_src.env[obj_model]._rec_name
                    res = pool_dest.get(obj_model).search(
                        [(rec_name, '=', names)], 1)
                    res = res and res[0] or False
                except Exception as e:
                    raise Warning(_(e))

            _logger.debug("name_get in src: %s", names)
            _logger.debug("name_search in dest: %s", res)
            if res:
                result = res
            else:
                _logger.warning(
                    "Record '%s' on relation %s not found, set to null.",
                    names, obj_model)
                _logger.warning(
                    "You should consider synchronize this model '%s'",
                    obj_model)
                self.report.append(
                    'WARNING: Record "%s" on relation %s not found, set to\
                     null.' % (names, obj_model))
        return result

    @api.model
    def data_transform(self, pool_src, pool_dest, obj, data, action=None,
                       destination_inverted=False, avoid_fields=[]):
        if action is None:
            action = {}
        if not destination_inverted:
            fields = pool_src.get('ir.model.fields').search_read(
                [('model_id.model', '=', obj),
                 ('name', 'not in', avoid_fields)],
                ['name', 'ttype', 'relation'])
        else:
            fields = pool_src.env['ir.model.fields'].search_read(
                [('model_id.model', '=', obj),
                 ('name', 'not in', avoid_fields)],
                ['name', 'ttype', 'relation'])
        _logger.debug("Transforming data")
        for field in fields:
            ftype = field.get('ttype')
            fname = field.get('name')
            if fname in avoid_fields:
                del data[fname]
            if ftype in ('function', 'one2many', 'one2one'):
                _logger.debug("Field %s of type %s, discarded.", fname, ftype)
                del data[fname]
            elif ftype == 'many2one':
                _logger.debug("Field %s is many2one", fname)
                if (isinstance(data[fname], list)) and data[fname]:
                    fdata = data[fname][0]
                else:
                    fdata = data[fname]
                df = self.relation_transform(pool_src, pool_dest,
                                             field.get('relation'), fdata,
                                             action, destination_inverted)
                data[fname] = df
                if not data[fname]:
                    del data[fname]
            elif ftype == 'many2many':
                data[fname] = [(6, 0, [
                    rec for rec in
                    map(lambda res: self.relation_transform(
                        pool_src, pool_dest, field.get(
                            'relation'),
                        res, action, destination_inverted),
                        data[fname]) if rec])]
        del data['id']
        return data

    @api.multi
    def upload_download(self):
        self.ensure_one()
        self.report = []
        start_date = fields.Datetime.now()
        server = self.server_url
        for obj_rec in server.obj_ids:
            _logger.debug("Start synchro of %s", obj_rec.name)
            self.synchronize(server, obj_rec)
            if obj_rec.action == 'b':
                time.sleep(1)
            obj_rec.write({'synchronize_date': fields.Datetime.now()})
        end_date = fields.Datetime.now()

        # Creating res.request for summary results
        if self.user_id:
            request = self.env['res.request']
            if not self.report:
                self.report.append('No exception.')
            summary = '''Here is the synchronization report:

Synchronization started: %s
Synchronization finished: %s

Synchronized records: %d
Records updated: %d
Records created: %d

Exceptions:
        ''' % (start_date, end_date, self.report_total, self.report_write,
               self.report_create)
            summary += '\n'.join(self.report)
            request.create({
                'name': "Synchronization report",
                'act_from': self.user_id.id,
                'date': fields.Datetime.now(),
                'act_to': self.user_id.id,
                'body': summary,
            })
            return {}

    @api.multi
    def upload_download_multi_thread(self):
        threaded_synchronization = threading.Thread(
            target=self.upload_download())
        threaded_synchronization.run()
        view_rec = self.env.ref('base_synchro.view_base_synchro_finish',
                                raise_if_not_found=False)
        action = self.env.ref(
            'base_synchro.action_view_base_synchro', raise_if_not_found=False
        ).read([])[0]
        action['views'] = [(view_rec and view_rec.id or False, 'form')]
        return action
