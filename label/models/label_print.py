# See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval


class LabelPrint(models.Model):
    _name = "label.print"
    _description = "Label Print"

    name = fields.Char(size=64, required=True, index=True)
    model_id = fields.Many2one(
        "ir.model",
        "Model",
        required=True,
        index=True,
        ondelete="cascade",
    )
    field_ids = fields.One2many(
        "label.print.field",
        "report_id",
        string="Fields",
    )
    ref_ir_act_report = fields.Many2one(
        "ir.actions.act_window",
        "Sidebar action",
        readonly=True,
        help=(
            "Sidebar action to make this template available on records "
            "of the related document model"
        ),
    )
    model_list = fields.Char(size=256)

    @api.onchange("model_id")
    def onchange_model(self):
        """
        Update model_list with current model and inherited models.
        """
        self.model_list = []
        if self.model_id:
            active_model = self.model_id.model
            active_model_obj = self.env[active_model]
            self.model_list = [active_model] + list(active_model_obj._inherits.keys())

    def create_action(self):
        action_obj = self.env["ir.actions.act_window"]

        for data in self:
            button_name = _("Label (%s)") % data.name

            action = action_obj.create(
                {
                    "name": button_name,
                    "type": "ir.actions.act_window",
                    "res_model": "label.print.wizard",
                    "binding_view_types": "form,list",
                    "context": "{'label_print': %d}" % data.id,
                    "view_mode": "form",
                    "target": "new",
                    "binding_model_id": data.model_id.id,
                    "binding_type": "action",
                }
            )
            data.ref_ir_act_report = action.id

        return True

    def unlink(self):
        self.mapped("ref_ir_act_report").filtered(lambda action: action.id).unlink()
        return super().unlink()

    def unlink_action(self):
        self.mapped("ref_ir_act_report").filtered(lambda action: action.id).unlink()
        return True


class LabelPrintField(models.Model):
    _name = "label.print.field"
    _rec_name = "sequence"
    _order = "sequence"
    _description = "Label Print Field One2many"

    sequence = fields.Integer(required=True)
    field_id = fields.Many2one("ir.model.fields", "Fields")
    report_id = fields.Many2one("label.print", "Report")
    model_id = fields.Many2one(
        related="report_id.model_id",
    )
    type = fields.Selection(
        [
            ("normal", "Normal"),
            ("barcode", "Barcode"),
            ("image", "Image"),
        ],
        required=True,
        default="normal",
    )
    python_expression = fields.Boolean()
    python_field = fields.Char("Fields", size=52)
    fontsize = fields.Float("Font Size", default=8.0)
    position = fields.Selection(
        [
            ("left", "Left"),
            ("right", "Right"),
            ("top", "Top"),
            ("bottom", "Bottom"),
        ]
    )
    nolabel = fields.Boolean("No Label")
    newline = fields.Boolean("New Line", default=True)

    @api.onchange("python_field")
    def _onchange_python_field(self):
        if self.python_field:
            python_field = self.python_field.split(".")

            if len(python_field) >= 3:
                python_field_str = python_field[1]
            else:
                python_field_str = python_field[-1]

            field_dict = self.env[self.model_id.model].fields_get()

            if python_field_str not in field_dict:
                raise ValidationError(_("Please enter valid field."))

        if self.python_field and not self.python_field.startswith("obj."):
            raise ValidationError(
                _(
                    "Python field value is wrong. "
                    "Please follow proper python expression."
                )
            )


class IrModelFields(models.Model):
    _inherit = "ir.model.fields"

    @api.model
    def name_search(
        self,
        name="",
        domain=None,
        operator="ilike",
        limit=100,
    ):
        domain = list(domain or [])

        data = self.env.context.get("model_list")
        if data:
            domain.append(("model", "in", safe_eval(data)))

        return super().name_search(
            name=name,
            domain=domain,
            operator=operator,
            limit=limit,
        )
