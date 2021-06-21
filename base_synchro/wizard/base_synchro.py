# See LICENSE file for full copyright and licensing details.

import logging
import threading
import time
from xmlrpc.client import ServerProxy
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _
from odoo.tools import format_datetime

_logger = logging.getLogger(__name__)


class RPCProxyOne(object):
    def __init__(self, server, ressource):
        """Class to store one RPC proxy server."""
        self.server = server
        local_url = "http://%s:%d/xmlrpc/common" % (
            server.server_url,
            server.server_port,
        )
        rpc = ServerProxy(local_url)
        self.uid = rpc.login(server.server_db, server.login, server.password)
        local_url = "http://%s:%d/xmlrpc/object" % (
            server.server_url,
            server.server_port,
        )
        self.rpc = ServerProxy(local_url)
        self.ressource = ressource

    def __getattr__(self, name):
        return lambda *args, **kwargs: self.rpc.execute(
            self.server.server_db,
            self.uid,
            self.server.password,
            self.ressource,
            name,
            *args
        )


class RPCProxy(object):
    """Class to store RPC proxy server."""

    def __init__(self, server):
        self.server = server

    def get(self, ressource):
        return RPCProxyOne(self.server, ressource)


class BaseSynchro(models.TransientModel):
    """Base Synchronization."""

    _name = "base.synchro"
    _description = "Base Synchronization"

    @api.depends("server_url")
    def _compute_report_vals(self):
        self.report_total = 0
        self.report_create = 0
        self.report_write = 0

    server_url = fields.Many2one(
        "base.synchro.server", "Server URL", required=True
    )
    user_id = fields.Many2one(
        "res.users", "Send Result To", default=lambda self: self.env.user
    )
    report_total = fields.Integer(compute="_compute_report_vals")
    report_create = fields.Integer(compute="_compute_report_vals")
    report_write = fields.Integer(compute="_compute_report_vals")

    @api.model
    def synchronize(self, server, object):
        pool = self
        sync_ids = []
        pool1 = RPCProxy(server)
        pool2 = pool
        dt = object.synchronize_date
        module = pool1.get("ir.module.module")
        model_obj = object.model_id.model
        module_id = module.search(
            [("name", "ilike", "base_synchro"), ("state", "=", "installed")]
        )
        if not module_id:
            raise ValidationError(
                _(
                    """If your Synchronization direction is/
                          download or both, please install
                          "Multi-DB Synchronization" module in targeted/
                        server!"""
                )
            )
        if object.action in ("d", "b"):
            sync_ids = pool1.get("base.synchro.obj").get_ids(
                model_obj, dt, eval(object.domain), {"action": "d"}
            )

        if object.action in ("u", "b"):
            _logger.debug(
                "Getting ids to synchronize [%s] (%s)",
                object.synchronize_date,
                object.domain,
            )
            sync_ids += pool2.env["base.synchro.obj"].get_ids(
                model_obj, dt, eval(object.domain), {"action": "u"}
            )
        sorted(sync_ids, key=lambda x: str(x[0]))
        for dt, id, action in sync_ids:
            destination_inverted = False
            if action == "d":
                pool_src = pool1
                pool_dest = pool2
            else:
                pool_src = pool2
                pool_dest = pool1
                destination_inverted = True
            fields = False
            if object.model_id.model == "crm.case.history":
                fields = ["email", "description", "log_id"]
            if not destination_inverted:
                value = pool_src.get(object.model_id.model).read([id], fields)[0]
            else:
                model_obj = pool_src.env[object.model_id.model]
                value = model_obj.browse([id]).read(fields)[0]
            if "create_date" in value:
                del value["create_date"]
            if "write_date" in value:
                del value["write_date"]
            for key, val in value.items():
                if isinstance(val, tuple):
                    value.update({key: val[0]})
            value = self.data_transform(
                pool_src,
                pool_dest,
                object.model_id.model,
                value,
                action,
                destination_inverted,
            )

            id2 = self.get_id(object.id, id, action)

            # Filter fields to not sync
            for field in object.avoid_ids:
                if field.name in value:
                    del value[field.name]
            if id2:
                _logger.debug(
                    "Updating model %s [%d]", object.model_id.name, id2
                )
                if not destination_inverted:
                    model_obj = pool_dest.env[object.model_id.model]
                    model_obj.browse([id2]).write(value)
                else:
                    pool_dest.get(object.model_id.model).write([id2], value)
                self.report_total += 1
                self.report_write += 1
            else:
                _logger.debug("Creating model %s", object.model_id.name)
                if not destination_inverted:
                    if object.model_id.model == "sale.order.line":
                        if value['product_template_id']:
                            value['product_id'] = value['product_template_id']
                            del value['product_template_id']
                            idnew = pool_dest.env[object.model_id.model].create(value)
                            new_id = idnew.id
                        else:
                            idnew = pool_dest.env[object.model_id.model].create(value)
                            new_id = idnew.id
                    elif object.model_id.model == "stock.move.line":
                        a = value.pop('product_qty')
                        b = value.pop('product_uom_qty')
                        idnew = pool_dest.env[object.model_id.model].create(value)
                        idnew.write({
                            'product_uom_qty': b
                        })
                        new_id = idnew.id
                    else:
                        idnew = pool_dest.env[object.model_id.model].create(value)
                        new_id = idnew.id
                else:
                    idnew = pool_dest.get(object.model_id.model).create(value)
                    new_id = idnew
                self.env["base.synchro.obj.line"].create(
                    {
                        "obj_id": object.id,
                        "local_id": (action == "u") and id or new_id,
                        "remote_id": (action == "d") and id or new_id,
                    }
                )
                self.report_total += 1
                self.report_create += 1
        return True

    @api.model
    def get_id(self, object_id, id, action):
        synchro_line_obj = self.env["base.synchro.obj.line"]
        field_src = (action == "u") and "local_id" or "remote_id"
        field_dest = (action == "d") and "local_id" or "remote_id"
        rec_id = synchro_line_obj.search(
            [("obj_id", "=", object_id), (field_src, "=", id)]
        )
        result = False
        if rec_id:
            result = synchro_line_obj.browse([rec_id[0].id]).read([field_dest])
            if result:
                result = result[0][field_dest]
        return result

    @api.model
    def relation_transform(
        self,
        pool_src,
        pool_dest,
        obj_model,
        res_id,
        action,
        destination_inverted,
    ):

        if not res_id:
            return False
        _logger.debug("Relation transform")
        self._cr.execute(
            """select o.id from base_synchro_obj o left join
                        ir_model m on (o.model_id =m.id) where
                        m.model=%s and o.active""",
            (obj_model,),
        )
        obj = self._cr.fetchone()
        result = False
        if obj:
            result = self.get_id(obj[0], res_id, action)
            _logger.debug(
                "Relation object already synchronized. Getting id%s", result
            )
            if obj_model == "stock.location":
                names = pool_src.get(obj_model).name_get([res_id])[0][1]
                res = pool_dest.env[obj_model]._name_search(names, [], "like")
                from_clause, where_clause, where_clause_params = res.get_sql()
                where_str = where_clause and (" WHERE %s" % where_clause) or ''
                query_str = 'SELECT "%s".id FROM ' % pool_dest.env[obj_model]._table + from_clause + where_str
                order_by = pool_dest.env[obj_model]._generate_order_by(None, query_str)
                query_str = query_str + order_by
                pool_dest.env[obj_model]._cr.execute(query_str, where_clause_params)
                res1 = self._cr.fetchall()
                res = [ls[0] for ls in res1]
                result = res[0]
            if obj_model == "stock.picking.type":
                names = pool_src.get(obj_model).name_get([res_id])[0][1]
                name = names.split(':')[0].strip()
                res = pool_dest.env[obj_model]._name_search(name, [], "like")
                from_clause, where_clause, where_clause_params = res.get_sql()
                where_str = where_clause and (" WHERE %s" % where_clause) or ''
                query_str = 'SELECT "%s".id FROM ' % pool_dest.env[obj_model]._table + from_clause + where_str
                order_by = pool_dest.env[obj_model]._generate_order_by(None, query_str)
                query_str = query_str + order_by
                pool_dest.env[obj_model]._cr.execute(query_str, where_clause_params)
                res1 = self._cr.fetchone()
                result = res1
        else:
            _logger.debug(
                """Relation object not synchronized. Searching/
             by name_get and name_search"""
            )
            report = []

            if not destination_inverted:
                if obj_model == "res.country.state":
                    names = pool_src.get(obj_model).name_get([res_id])[0][1]
                    name = names.split("(")[0].strip()
                    res = pool_dest.env[obj_model]._name_search(name, [], "like")
                    res = [res]
                elif obj_model == "res.country":
                    names = pool_src.get(obj_model).name_get([res_id])[0][1]
                    res = pool_dest.env[obj_model]._name_search(names, [], "=")
                    res = [[res[0]]]
                else:
                    names = pool_src.get(obj_model).name_get([res_id])[0][1]
                    res = pool_dest.env[obj_model].name_search(names, [], "like")
            else:
                model_obj = pool_src.env[obj_model]
                names = model_obj.browse([res_id]).name_get()[0][1]
                res = pool_dest.env[obj_model].name_search(names, [], "like")
            _logger.debug("name_get in src: %s", names)
            _logger.debug("name_search in dest: %s", res)
            if res:
                result = res[0][0]
            else:
                _logger.warning(
                    """Record '%s' on relation %s not found, set/
                                to null.""",
                    names,
                    obj_model,
                )
                _logger.warning(
                    """You should consider synchronize this/
                model '%s""",
                    obj_model,
                )
                report.append(
                    """WARNING: Record "%s" on relation %s not/
                    found, set to null."""
                    % (names, obj_model)
                )
        return result

    @api.model
    def data_transform(
        self,
        pool_src,
        pool_dest,
        obj,
        data,
        action=None,
        destination_inverted=False,
    ):
        if action is None:
            action = {}
        if not destination_inverted:
            fields = pool_src.get(obj).fields_get()
        else:
            fields = pool_src.env[obj].fields_get()
        _logger.debug("Transforming data")
        for f in fields:
            ftype = fields[f]["type"]
            if ftype in ("function", "one2many", "one2one"):
                _logger.debug("Field %s of type %s, discarded.", f, ftype)
                del data[f]
            elif ftype == "many2one":
                _logger.debug("Field %s is many2one", f)
                if (isinstance(data[f], list)) and data[f]:
                    fdata = data[f][0]
                else:
                    fdata = data[f]

                df = self.relation_transform(
                    pool_src,
                    pool_dest,
                    fields[f]["relation"],
                    fdata,
                    action,
                    destination_inverted,
                )
                if obj == "stock.picking":
                    data[f] = df
                    if not data[f]:
                        del data[f]
                else:
                    data[f] = df
                    if not data[f]:
                        del data[f]

            elif ftype == "many2many":
                res = map(
                    lambda x: self.relation_transform(
                        pool_src,
                        pool_dest,
                        fields[f]["relation"],
                        x,
                        action,
                        destination_inverted,
                    ),
                    data[f],
                )
                data[f] = [(6, 0, [x for x in res if x])]
        del data["id"]
        return data

    def upload_download(self):
        self.ensure_one()
        report = []
        start_date = fields.Datetime.now()
        timezone = self._context.get("tz", "UTC")
        start_date = format_datetime(
            self.env, start_date, timezone, dt_format=False
        )
        server = self.server_url
        for obj_rec in server.obj_ids:
            _logger.debug("Start synchro of %s", obj_rec.name)
            dt = fields.Datetime.now()
            self.synchronize(server, obj_rec)
            if obj_rec.action == "b":
                time.sleep(1)
                dt = fields.Datetime.now()
            obj_rec.write({"synchronize_date": dt})
        end_date = fields.Datetime.now()
        end_date = format_datetime(
            self.env, end_date, timezone, dt_format=False
        )
        # Creating res.request for summary results
        if self.user_id:
            request = self.env["res.request"]
            if not report:
                report.append("No exception.")
            summary = """Here is the synchronization report:

     Synchronization started: %s
     Synchronization finished: %s

     Synchronized records: %d
     Records updated: %d
     Records created: %d

     Exceptions:
        """ % (
                start_date,
                end_date,
                self.report_total,
                self.report_write,
                self.report_create,
            )
            summary += "\n".join(report)
            request.create(
                {
                    "name": "Synchronization report",
                    "act_from": self.env.user.id,
                    "date": fields.Datetime.now(),
                    "act_to": self.user_id.id,
                    "body": summary,
                }
            )
            return {}

    def upload_download_multi_thread(self):
        threaded_synchronization = threading.Thread(
            target=self.upload_download()
        )
        threaded_synchronization.run()
        id2 = self.env.ref("base_synchro.view_base_synchro_finish").id
        return {
            "binding_view_types": "form",
            "view_mode": "form",
            "res_model": "base.synchro",
            "views": [(id2, "form")],
            "view_id": False,
            "type": "ir.actions.act_window",
            "target": "new",
        }
