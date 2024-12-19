# See LICENSE file for full copyright and licensing details.

import time
import logging
import threading
from xmlrpc.client import ServerProxy
from odoo import api, fields, models
# from odoo.exceptions import Warning
# TODO:
from odoo.exceptions import ValidationError
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class RPCProxyOne(object):
    def __init__(self, server, ressource):
        """Class to store one RPC proxy server."""
        self.server = server
        local_url = "http://%s:%d/xmlrpc/common" % (
            server.server_url,
            server.server_port,
        )
        # print("================local_url==============", local_url)
        rpc = ServerProxy(local_url)
        self.uid = rpc.login(server.server_db, server.login, server.password)
        local_url = "http://%s:%d/xmlrpc/object" % (
            server.server_url,
            server.server_port,
        )
        # print("local_url**********************", local_url)
        self.rpc = ServerProxy(local_url)
        # print("self.rpc---------------", self.rpc)
        self.ressource = ressource
        # print("self.ressource!!!!!!!!!!!!!!!!!!!!", self.ressource)

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

    server_url = fields.Many2one(
        "base.synchro.server", "Server URL", required=True
    )
    user_id = fields.Many2one(
        "res.users",
        "Send Result To",
        default=lambda self: self.env.user
    )

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
            raise Warning(
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
            for field in object.avoid_ids:
                if field.name in value:
                    del value[field.name]
            if id2:
                if not destination_inverted:
                    model_obj = pool_dest.env[object.model_id.model]
                    model_obj.browse([id2]).write(value)
                else:
                    pool_dest.get(object.model_id.model).write([id2], value)
                self.report_total += 1
                self.report_write += 1
            else:
                if not destination_inverted:
                    idnew = pool_dest.env[object.model_id.model].create(value)
                    print("\n\n idnew 2222222222222222222222222222222 ", idnew)
                    8/0
                else:
                    idnew = pool_dest.get(object.model_id.model).create(value)
                    print("\n\n idnew11111111111111111111111111", idnew)
                    # 10/0

                self.env["base.synchro.obj.line"].create(
                    {
                        "obj_id": object.id,
                        "local_id": (action == "u") and id or idnew,
                        "remote_id": (action == "d") and id or idnew,
                    }
                )
                self.report_total += 1
                self.report_create += 1
        return True

    report_total = fields.Integer(compute="_compute_report_vals")
    report_create = fields.Integer(compute="_compute_report_vals")
    report_write = fields.Integer(compute="_compute_report_vals")

    @api.depends("server_url")
    def _compute_report_vals(self):
        self.report_total = 0
        self.report_create = 0
        self.report_write = 0

    @api.model
    def get_id(self, object_id, id, action):
        synchro_line_obj = self.env["base.synchro.obj.line"]
        # print("synchro_line_obj:::::::::::::", synchro_line_obj)
        field_src = (action == "u") and "local_id" or "remote_id"
        # print("field_src:::::::::::::::::", field_src)
        field_dest = (action == "d") and "local_id" or "remote_id"
        # print("field_dest::::::::::::::::", field_dest)
        rec_id = synchro_line_obj.search([("obj_id", "=", object_id),
                                          (field_src, "=", id)])
        # print("rec_id:::::::::::::::", rec_id)
        result = False
        if rec_id:
            result = synchro_line_obj.browse([rec_id[0].id]).read([field_dest])
            # print("result::::::::::::::::", result)
            if result:
                result = result[0][field_dest]
                # print("result`````````````````````````````", result)
        return result

    @api.model
    def relation_transform(
            self, pool_src, pool_dest, obj_model,
            res_id, action, destination_inverted
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
                "Relation object already synchronized. Getting id%s", result)
        else:
            _logger.debug(
                """Relation object not synchronized. Searching/
             by name_get and name_search"""
            )
            report = []
            if not destination_inverted:
                names = pool_src.get(obj_model).name_get([res_id])[0][1]
                res = None
                try:
                    res = pool_dest.env[obj_model].name_search(names, [], "like")
                except Exception:
                    pass
            else:
                model_obj = pool_src.env[obj_model]
                names = model_obj.browse([res_id]).name_get()[0][1]
                res = pool_dest.get(obj_model).name_search(names, [], "like")
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
                    """ValidationError: Record "%s" on relation %s not/
                    found, set to null."""
                    % (names, obj_model)
                )
        return result

    @api.model
    def data_transform(
            self, pool_src, pool_dest, obj, data,
            action=None, destination_inverted=False
    ):
        if action is None:
            action = {}
        if not destination_inverted:
            fields = pool_src.get(obj).fields_get()
            # print("fields::::::::::::::::::::::::::::::fields::::::::::::::::", fields)
        else:
            fields = pool_src.env[obj].fields_get()
            # print("fields===========fields=============fields============", fields)
        _logger.debug("Transforming data")
        for f in fields:
            ftype = fields[f]["type"]
            # print("ftype88888888888888", ftype)
            # if f == 'type':
            #     # print("fffffffffffffffffffffff", f)
            #     f = "move_type"
            if ftype in ("function", "one2many", "one2one"):
                # print("ftype----------------", ftype)
                _logger.debug("Field %s of type %s, discarded.", f, ftype)
                del data[f]
            elif ftype == "many2one":
                # print("ftype:::::::::many2one::::::::::;many2one:::::::::many2one:::::::::", ftype)
                _logger.debug("Field %s is many2one", f)
                if (isinstance(data[f], list)) and data[f]:
                    fdata = data[f][0]
                    # print("fdata........fdata...............fdata...........fdata.............", fdata)
                else:
                    fdata = data[f]
                    # print("fdata-----fdata-------fdata-----------------fdata--------", fdata)
                df = self.relation_transform(
                    pool_src,
                    pool_dest,
                    fields[f]["relation"],
                    fdata,
                    action,
                    destination_inverted,
                )
                # print("df##########################", df)
                data[f] = df
                # print("data[f]!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", data[f])
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
                # print("res$$$$$$$$$$$$$$$$$$$$$", res)
                data[f] = [(6, 0, [x for x in res if x])]
                # print("data[f]????????????/data[f]?????????????????data[f]??????????", data[f])

            # if obj and obj == "account.move" and f == "invoice_payment_state":
            #     print("obj===============>>>>>>>>>>>", obj)
            #     if 'payment_state' in data and data.get('payment_state') == 'not_paid':
            #         data.update({'payment_state': 'not_paid'})
            #amount_total_signed

            if obj and obj == "account.move.line" and f == "display_type":
                if 'display_type' in data and data.get('display_type') == False:
                    data.update({'display_type': False})

            # display_type = fields.Selection([
            #     ('line_section', 'Section'),
            #     ('line_note', 'Note'),
            # ], default=False, help="Technical field for UX purpose.")

            # display_type = fields.Selection(
            #     selection=[
            #         ('product', 'Product'),
            #         ('cogs', 'Cost of Goods Sold'),
            #         ('tax', 'Tax'),
            #         ('discount', "Discount"),
            #         ('rounding', "Rounding"),
            #         ('payment_term', 'Payment Term'),
            #         ('line_section', 'Section'),
            #         ('line_note', 'Note'),
            #         ('epd', 'Early Payment Discount')
            #     ],
            #     compute='_compute_display_type', store=True, readonly=False, precompute=True,
            #     required=True,
            # )
            # if obj and obj == "account.partial.reconcile" and f == "":
            #     if ''

        del data["id"]
        if obj and obj == "account.move":
            # print("=========================== obj =============data======", obj, data)
            payment_state = data.get("invoice_payment_state")
            print(" payment ============================ ", payment_state)
            move_type = data.get("type", "out_invoice")
            data.update({"move_type": move_type})
            if move_type != "entry":
                data.update({"payment_state": payment_state})
            if "type" in data.keys():
                data.pop("type")
            if "invoice_payment_state" in data.keys():
                data.pop("invoice_payment_state")
        print("\n\n=========FINAL===DATA======", data)



        # TODO: wrong
        # old_invoices = self.env['account.move'].search([('payment_state', '!=', False)])
        # for invoice in old_invoices:
        #     payment_state = 'paid' if invoice.payment_state == 'paid' else 'not_paid'
        #     invoice.write({'payment_state': payment_state})
            # total_amount_field = 'amount_total_signed' if hasattr(invoice, 'amount_total_signed') else 'amount_total'
            # total_amount = invoice[total_amount_field]
            # print("Total Amount for Invoice {}: {}".format(invoice.id, total_amount))

        return data

    # @api.model
    # def update_hs_code(self):
    #     # Execute the query to update hs_code from x_studio_hs_code
    #     self.env.cr.execute("""
    #             UPDATE product_template
    #             SET hs_code = x_studio_hs_code
    #             WHERE x_studio_hs_code IS NOT NULL
    #         """)

    @api.model
    def update_invoice_payment_state(self):
        cr = self.env.cr
        query = """
        UPDATE account_move 
        SET payment_state = invoice_payment_state 
        WHERE invoice_payment_state IS NOT NULL
        """
        cr.execute(query)
        self.env.cr.commit()

    def upload_download(self):
        # print("self:::::::::::::::::::::", self)
        self.ensure_one()
        report = []
        start_date = fields.Datetime.now()
        server = self.server_url
        # print("server::::::::::::::", server)
        for obj_rec in server.obj_ids:
            # print("obj_rec:::::::::::::", obj_rec)
            _logger.debug("Start synchro of %s", obj_rec.name)
            dt = fields.Datetime.now()
            self.synchronize(server, obj_rec)
            if obj_rec.action == "b":
                time.sleep(1)
                dt = fields.Datetime.now()
            obj_rec.write({"synchronize_date": dt})
        end_date = fields.Datetime.now()
        # print("end_date::::::::", end_date)

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
        # print("::::::::::::::;self:::::::::::::", self)
        threaded_synchronization = threading.Thread(target=self.upload_download())
        # print("threaded_synchronization::::::::::::::::", threaded_synchronization)
        threaded_synchronization.start()
        id2 = self.env.ref("base_synchro.view_base_synchro_finish").id
        # print("id2::::::::::::::::::", id2)
        return {
            "binding_view_types": "form",
            "view_mode": "form",
            "res_model": "base.synchro",
            "views": [(id2, "form")],
            "view_id": False,
            "type": "ir.actions.act_window",
            "target": "new",
        }
