# See LICENSE file for full copyright and licensing details.

import time

from odoo import api, fields, models


class BaseSynchroServer(models.Model):
    """Class to store the information regarding server."""

    _name = "base.synchro.server"
    _description = "Synchronized server"

    name = fields.Char(string="Server name", required=True)
    server_url = fields.Char(string="Server URL", required=True)
    server_port = fields.Integer(string="Server Port", required=True, default=8069)
    server_db = fields.Char(string="Server Database", required=True)
    login = fields.Char(string="User Name", required=True)
    password = fields.Char(string="Password", required=True)
    obj_ids = fields.One2many(
        "base.synchro.obj", "server_id", string="Models", ondelete="cascade"
    )


class BaseSynchroObj(models.Model):
    """Class to store the operations done by wizard."""

    _name = "base.synchro.obj"
    _description = "Register Class"
    _order = "sequence"

    name = fields.Char(string="Name", required=True)
    domain = fields.Char(string="Domain", required=True, default="[]")
    server_id = fields.Many2one(
        "base.synchro.server", string="Server", ondelete="cascade", required=True
    )
    model_id = fields.Many2one(
        "ir.model", string="Object to synchronize", required=True
    )
    action = fields.Selection(
        [("d", "Download"), ("u", "Upload"), ("b", "Both")],
        string="Synchronization direction",
        required=True,
        default="d",
    )
    sequence = fields.Integer(string="Sequence")
    active = fields.Boolean(string="Active", default=True)
    synchronize_date = fields.Datetime(string="Latest Synchronization", readonly=True)
    line_id = fields.One2many(
        "base.synchro.obj.line", "obj_id", string="IDs Affected", ondelete="cascade"
    )
    avoid_ids = fields.One2many(
        "base.synchro.obj.avoid", "obj_id", string="Fields Not Sync."
    )

    @api.model
    def get_ids(self, obj, dt, domain=None, action=None):
        if action is None:
            action = {}
        pool = self.env[obj]
        result = []
        if dt:
            w_date = domain + [("write_date", ">=", dt)]
            c_date = domain + [("create_date", ">=", dt)]
        else:
            w_date = c_date = domain
        obj_rec = pool.search(w_date)
        obj_rec += pool.search(c_date)
        for r in obj_rec.read(["create_date", "write_date"]):
            result.append(
                (
                    r["write_date"] or r["create_date"],
                    r["id"],
                    action.get("action", "d"),
                )
            )
        return result


class BaseSynchroObjAvoid(models.Model):
    """Class to avoid the base synchro object."""

    _name = "base.synchro.obj.avoid"
    _description = "Fields to not synchronize"

    name = fields.Char(string="Field Name", required=True)
    obj_id = fields.Many2one(
        "base.synchro.obj", string="Object", required=True, ondelete="cascade"
    )


class BaseSynchroObjLine(models.Model):
    """Class to store object line in base synchro."""

    _name = "base.synchro.obj.line"
    _description = "Synchronized instances"

    name = fields.Datetime(
        string="Date",
        required=True,
        default=lambda *args: time.strftime("%Y-%m-%d %H:%M:%S"),
    )
    obj_id = fields.Many2one("base.synchro.obj", string="Object", ondelete="cascade")
    local_id = fields.Integer(string="Local ID", readonly=True)
    remote_id = fields.Integer(string="Remote ID", readonly=True)
