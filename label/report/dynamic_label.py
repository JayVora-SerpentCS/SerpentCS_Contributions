# 1: imports of odoo
import base64
import time

from reportlab.graphics.barcode import createBarcodeDrawing

from odoo import _, api, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class ReportDynamicLabel(models.AbstractModel):
    _name = "report.label.report_label"
    _description = "Print Label Report Class"

    def _get_field_data(self, field, record):
        """Return rendered data for one configured label field."""
        position_style = ""
        if field.python_expression and field.python_field:
            string = field.python_field.split(".")[-1]
            value = safe_eval(field.python_field, {"obj": record})
        elif field.field_id.name:
            string = field.field_id.field_description
            value = getattr(record, field.field_id.name)
        else:
            return None, None

        if not value:
            return None, None

        display_type = field.type
        field_name = (
            field.field_id.name or field.field_id.field_description
            if field.field_id
            else ""
        )
        if (
            display_type == "normal"
            and field.field_id
            and "barcode" in field_name.lower()
        ):
            display_type = "barcode"

        image_mimetype = "image/png"
        if hasattr(value, "to_base64"):
            image_mimetype = value.mimetype or image_mimetype
            is_image_field = (
                field.type == "image"
                or (
                    field.field_id
                    and field.field_id.ttype == "binary"
                    and "image" in field_name.lower()
                )
                or image_mimetype.startswith("image/")
            )
            if is_image_field:
                display_type = "image"
                value = value.to_base64()

        if isinstance(value, models.BaseModel):
            value = value.display_name
        value = value or ""

        barcode_image = ""
        barcode_mimetype = "image/png"
        if display_type == "barcode":
            barcode_image = base64.b64encode(
                createBarcodeDrawing(
                    "Code128",
                    value=str(value),
                    format="svg",
                    width=600,
                    height=100,
                    humanReadable=False,
                )
                .asString("svg")
                .encode("utf-8")
            ).decode("ascii")
            barcode_mimetype = "image/svg+xml"

        position = field.position
        if not position and display_type == "image":
            position = "right"
        elif not position and display_type == "barcode":
            position = "left"

        string = "" if field.nolabel else string + " :- "
        bottom_data = None
        if display_type in ["image", "barcode"]:
            string = ""
            if position != "bottom":
                bottom_data = {}
                if position in ("left", "right"):
                    position_style = f"float:{position};"
            else:
                bottom_data = {
                    "string": string,
                    "value": value,
                    "barcode_image": barcode_image,
                    "barcode_mimetype": barcode_mimetype,
                    "bottom": True,
                    "type": display_type,
                    "mimetype": image_mimetype,
                    "newline": field.newline,
                    "style": f"font-size:{field.fontsize}px;{position_style}",
                }

        field_data = {
            "string": string,
            "value": value,
            "barcode_image": barcode_image,
            "barcode_mimetype": barcode_mimetype,
            "type": display_type,
            "mimetype": image_mimetype,
            "newline": field.newline,
            "style": f"font-size:{field.fontsize}px;{position_style}",
        }
        return field_data, bottom_data

    def get_data(self, row, columns, ids, model, number_of_copy):
        active_model_obj = self.env[model]
        label_print_obj = self.env["label.print"]
        label_print_id = self.env.context.get("label_print") or self.env.context.get(
            "label_print_id"
        )
        label_print_data = label_print_obj.browse(label_print_id).exists()
        if not label_print_data:
            raise UserError(_("The label print configuration could not be found."))
        if not label_print_data.field_ids:
            raise UserError(
                _(
                    "No fields are configured for this label. "
                    "Add at least one field in the Label Print configuration."
                )
            )

        result = []
        value_vals = []

        for datas in active_model_obj.browse(ids):

            for _i in range(number_of_copy):
                vals = []
                bot_dict = {}

                for field in label_print_data.field_ids:
                    field_data, field_bot_dict = self._get_field_data(field, datas)
                    if field_bot_dict is not None:
                        bot_dict = field_bot_dict
                    if field_data and not bot_dict:
                        vals.append(field_data)

                if bot_dict:
                    vals.append(bot_dict)

                if vals and vals[0]["value"] not in value_vals:
                    value_vals.append(vals[0]["value"])

                result.append(vals)
                temp = vals

        new_list = [
            result[i * columns : (i + 1) * columns]
            for i in range((len(result) + columns - 1) // columns)
        ]

        list_newdata = [
            item["value"]
            for sublist in new_list
            for subsublist in sublist
            for item in subsublist
        ]

        newlist_len = len(list_newdata)

        diff = number_of_copy - newlist_len if newlist_len <= number_of_copy else 0

        if len(ids) == 1:
            result.extend([temp] * diff)

        return new_list

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data or not data.get("form") or not self.env.context.get("active_model"):
            raise UserError(
                _("Form content is missing, this report cannot be printed.")
            )

        model = self.env.context.get("active_model")
        docs = self.env[model].browse(self.env.context.get("active_ids", []))

        return {
            "doc_ids": docs.ids,
            "doc_model": model,
            "data": data,
            "docs": docs,
            "time": time,
            "get_data": self.get_data,
        }
