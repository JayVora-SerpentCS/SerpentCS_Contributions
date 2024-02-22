# See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.tools.safe_eval import safe_eval as eval
from odoo.exceptions import UserError, ValidationError


class LabelPrint(models.Model):
    _name = "label.print"
    _description = "Label Print"

    name = fields.Char("Name", size=64, required=True, index=True)
    model_id = fields.Many2one("ir.model", "Model", required=True, index=True,
                               ondelete='cascade')
    field_ids = fields.One2many(
        "label.print.field", "report_id", string="Fields")
    ref_ir_act_report = fields.Many2one(
        "ir.actions.act_window",
        "Sidebar action",
        readonly=True,
        help="""Sidebar action to make this
                                        template available on records
                                        of the related document model""",
    )
    model_list = fields.Char("Model List", size=256)

    @api.onchange("model_id")
    def onchange_model(self):
        model_list = []
        if self.model_id:
            model_obj = self.env["ir.model"]
            current_model = self.model_id.model
            model_list.append(current_model)
            active_model_obj = self.env[self.model_id.model]
            if active_model_obj._inherits:
                for key, val in active_model_obj._inherits.items():
                    model_ids = model_obj.search([("model", "=", key)])
                    if model_ids:
                        model_list.append(key)
        self.model_list = model_list

    def create_action(self):
        vals = {}
        action_obj = self.env["ir.actions.act_window"]
        for data in self.browse(self.ids):
            button_name = _("Label (%s)") % data.name
            vals["ref_ir_act_report"] = action_obj.create(
                {
                    "name": button_name,
                    "type": "ir.actions.act_window",
                    "res_model": "label.print.wizard",
                    "binding_view_types": "form,list",
                    "context": "{'label_print' : %d}" % (data.id),
                    "view_mode": "form",
                    "target": "new",
                    "binding_model_id": data.model_id.id,
                    "binding_type": "action",
                }
            )
        self.write({"ref_ir_act_report": vals.get(
            "ref_ir_act_report", False).id})
        return True

    def unlink_action(self):
        actions_to_unlink = [template.ref_ir_act_report for template in self if template.ref_ir_act_report.id]
        for action in actions_to_unlink:
            action.unlink()
        return True


class LabelPrintField(models.Model):
    _name = "label.print.field"
    _rec_name = "sequence"
    _order = "sequence"
    _description = "Label Print Field One2many"

    sequence = fields.Integer("Sequence", required=True)
    field_id = fields.Many2one("ir.model.fields", "Fields", required=False)
    report_id = fields.Many2one("label.print", "Report")
    model_id = fields.Many2one(related="report_id.model_id", string="Model")
    type = fields.Selection(
        [("normal", "Normal"), ("barcode", "Barcode"), ("image", "Image")],
        "Type",
        required=True,
        default="normal",
    )
    python_expression = fields.Boolean("Python Expression")
    python_field = fields.Char("Fields", size=52)
    fontsize = fields.Float("Font Size", default=8.0)
    position = fields.Selection(
        [("left", "Left"), ("right", "Right"),
         ("top", "Top"), ("bottom", "Bottom")],
        "Position",
    )
    nolabel = fields.Boolean("No Label")
    newline = fields.Boolean("New Line", deafult=True)
    
    @api.onchange("python_field")
    def _onchange_python_field(self):
        field_str = self.python_field
        if field_str:
            python_field = field_str.split(".")
            if len(python_field) >=3 :
                python_field_str = python_field[1] 
            else:
                python_field_str = python_field[-1]
            model_id = self.model_id
            fields = self.env[model_id.model].fields_get()
            key_list = []
            for key,v in fields.items():
                key_list.append(key)
            if not python_field_str in key_list:
                raise ValidationError(_("Please enter valid field."))
        if self.python_field and not self.python_field.startswith("obj."):
            raise ValidationError(_("Python field value is wrong. Please follow proper python expression."))


class IrModelFields(models.Model):
    _inherit = "ir.model.fields"

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=None):
        data = self._context.get("model_list")
        if data:
            args.append(("model", "in", eval(data)))
        ret_vat = super(IrModelFields, self).name_search(
            name=name, args=args, operator=operator, limit=limit
        )
        return ret_vat
