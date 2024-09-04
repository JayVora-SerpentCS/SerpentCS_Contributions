# See LICENSE file for full copyright and licensing details.

# 1:  imports of odoo
import time

from odoo import _, api, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval as eval


class ReportDynamicLabel(models.AbstractModel):
    _name = "report.label.report_label"
    _description = "Print Label Report Class"

    def get_data(self, row, columns, ids, model, number_of_copy):
        active_model_obj = self.env[model]
        label_print_obj = self.env["label.print"]
        label_print_data = label_print_obj.browse(self.env.context.get("label_print"))
        result = []
        value_vals = []
        for datas in active_model_obj.browse(ids):
            for i in range(number_of_copy):
                vals = []
                bot_dict = {}
                for field in label_print_data.field_ids:
                    value = ""
                    pos = ""
                    if field.python_expression and field.python_field:
                        string = field.python_field.split(".")[-1]
                        value = eval(field.python_field, {"obj": datas})
                    elif field.field_id.name:
                        string = field.field_id.field_description
                        value = getattr(datas, field.field_id.name)
                    if not value:
                        continue
                    if isinstance(value, dict):
                        model_obj = self.env[value._name]
                        value = eval("obj." + model_obj._rec_name, {"obj": value})
                    value = value or ""
                    if field.nolabel:
                        string = ""
                    else:
                        string += " :- "
                    if field.type in ["image", "barcode"]:
                        string = ""
                        if field.position != "bottom":
                            pos = f"float:{field.position};"
                            bot_dict = {}
                        else:
                            bot_dict = {
                                "string": string,
                                "value": value,
                                "bottom": True,
                                "type": field.type,
                                "newline": field.newline,
                                "style": f"font-size:{field.fontsize}px;{pos}",
                            }
                    if not bot_dict:
                        vals.append({
                            "string": string,
                            "value": value,
                            "type": field.type,
                            "newline": field.newline,
                            "style": f"font-size:{field.fontsize}px;{pos}",
                        })
                if bot_dict:
                    vals.append(bot_dict)
                if vals and vals[0]["value"] not in value_vals:
                    value_vals.append(vals[0]["value"])
                result.append(vals)
                temp = vals
        new_list = [
            result[i * columns:(i + 1) * columns]
            for i in range((len(result) + columns - 1) // columns)
        ]
        list_newdata = [item["value"] for sublist in new_list for subsublist in sublist for item in subsublist]
        newlist_len = len(list_newdata)
        remain_data = []
        for newlist_data in set(list_newdata):
            count = list_newdata.count(newlist_data)
            if count < number_of_copy:
                remain_data.extend([newlist_data] * (number_of_copy - count))
        for data_value_vals in value_vals:
            if data_value_vals not in list_newdata:
                remain_data.extend([data_value_vals] * number_of_copy)
        diff = number_of_copy - newlist_len if newlist_len <= number_of_copy else 0
        if len(ids) == 1:
            result.extend([temp] * diff)
        return new_list


    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get("form") or not self.env.context.get("active_model"):
            raise UserError(
                _(
                    "Form content is missing, \
                        this report cannot be printed."
                )
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
