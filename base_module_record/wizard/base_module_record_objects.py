# See LICENSE file for full copyright and licensing details.

from . import base_module_save
from odoo import api, fields, models
from odoo.tools import ustr
from odoo.tools.translate import _


class BaseModuleRecord(models.TransientModel):
    _name = "base.module.record"
    _description = "Base Module Record"

    @api.model
    def _get_default_objects(self):
        names = (
            "ir.ui.view",
            "ir.ui.menu",
            "ir.model",
            "ir.model.fields",
            "ir.model.access",
            "res.partner",
            "res.partner.category",
            "ir.actions.server",
            "ir.server.object.lines"
    )
        return self.env["ir.model"].search([("model", "in", names)])

    check_date = fields.Datetime(
        "Record from Date", required=True, default=fields.Datetime.now
    )
    objects = fields.Many2many(
        "ir.model",
        "base_module_record_object_rel",
        "objects",
        "model_id",
        default=_get_default_objects,
    )
    filter_cond = fields.Selection(
        [
            ("created", "Created"),
            ("modified", "Modified"),
            ("created_modified", "Created & Modified"),
        ],
        "Records only",
        required=True,
        default="created",
    )

    def record_objects(self):
        data = self.read([])[0]
        filter_cond = data.get("filter_cond")
        check_date = data.get("check_date")
        mod_obj = self.env["ir.model"]
        recording_data = []
        for obj_id in data["objects"]:
            obj_name = (mod_obj.browse(obj_id)).model
            obj_pool = self.env[obj_name]
            if filter_cond == "created":
                search_condition = [(
                                "create_date", ">", check_date)]
            elif filter_cond == "modified":
                search_condition = [(
                                "write_date", ">", check_date)]
            elif filter_cond == "created_modified":
                search_condition = ["|", 
                                ("create_date", ">", check_date),
                                ("write_date", ">", check_date)]
            if "_log_access" in dir(obj_pool):
                if not (obj_pool._log_access):
                    search_condition = []
                if "_auto" in dir(obj_pool):
                    if not obj_pool._auto:
                        continue
            search_ids = obj_pool.search(search_condition)
            for s_id in search_ids:
                dbname = self.env.cr.dbname
                args = (dbname, self.env.user.id, obj_name, 'copy',
                        s_id.id, {})
                recording_data.append(('query', args, {}, s_id.id))

        if recording_data:
            res_id = self.env.ref("base_module_record.info_start_form_view",
                                  raise_if_not_found=False).id
            self = self.with_context({"recording_data": recording_data})
            return {
                "name": _("Module Recording"),
                "context": self._context,
                "binding_view_types": "form",
                "view_mode": "form",
                "res_model": "base.module.record.objects",
                "views": [(res_id, "form")],
                "type": "ir.actions.act_window",
                "target": "new",
            }
        res_id = self.env.ref(
                    "base_module_record.module_recording_message_view",
                    raise_if_not_found=False).id
        return {
            "name": _("Module Recording"),
            "context": self._context,
            "binding_view_types": "form",
            "view_mode": "form",
            "res_model": "base.module.record.objects",
            "views": [(res_id, "form")],
            "type": "ir.actions.act_window",
            "target": "new",
        }


class BaseModuleRecordObjects(models.TransientModel):
    _name = "base.module.record.objects"
    _description = "Base Module Record Objects"

    def inter_call(self):
        ctx = dict(self._context)
        ctx.update({"depends": {}})
        data = self.ids
        res = base_module_save._create_module(self.with_context(ctx), data)
        res_id = self.env.ref("base_module_record.module_create_form_view",
                              raise_if_not_found=False).id
        rec_id = self.create({
            "module_filename": ustr(res.get("module_filename")),
            "module_file": ustr(res.get("module_file")),
            "name": ustr(res.get("name")),
            "directory_name": ustr(res.get("directory_name")),
            "version": ustr(res.get("version")),
            "author": ustr(res.get("author")),
            "website": ustr(res.get("website")),
            "category": ustr(res.get("category")),
            "description": ustr(res.get("description")),
        }).id
        return {
            "name": _("Module Recording"),
            "binding_view_types": "form",
            "view_mode": "form",
            "res_id": rec_id,
            "res_model": "base.module.record.objects",
            "views": [(res_id, "form")],
            "type": "ir.actions.act_window",
            "target": "new",
        }

    def _valid_field_parameter(self, field, name):
        # I can't even
        return name == 'filename' or super()._valid_field_parameter(field, name)

    name = fields.Char("Module Name", size=64)
    directory_name = fields.Char(size=32)
    version = fields.Char(default="14.0", size=16)
    author = fields.Char(size=64, required=True, default="Odoo SA")
    category = fields.Char(
        size=64,
        required=True,
        default="Vertical Modules/Parametrization"
    )
    website = fields.Char(
        "Documentation URL",
        size=64,
        required=True,
        default="https://www.odoo.com"
    )
    description = fields.Text("Full Description")
    data_kind = fields.Selection(
        [("demo", "Demo Data"), ("update", "Normal Data")],
        "Type of Data",
        required=True,
        default="update"
    )
    module_file = fields.Binary("Module .zip File", filename="module_filename")
    module_filename = fields.Char("Filename", size=64)

