# See LICENSE file for full copyright and licensing details.

# 1:  imports of odoo
import time
from odoo import models, api, _
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval as eval


class ReportDynamicLabel(models.AbstractModel):
    _name = 'report.label.report_label'

    def get_data(self, row, columns, ids, model, number_of_copy):
        active_model_obj = self.env[model]
        label_print_obj = self.env['label.print']
        label_print_data = label_print_obj.\
            browse(self.env.context.get('label_print'))
        result = []
        value_vals = []
        diff = 0
        for datas in active_model_obj.browse(ids):
            for i in range(0, number_of_copy):
                vals = []
                bot = False
                bot_dict = {}
                for field in label_print_data.field_ids:
                    string = ''
                    pos = ''
                    if field.python_expression and field.python_field:
                        string = field.python_field.split('.')[-1]
                        value = eval(field.python_field, {'obj': datas})

                    elif field.field_id.name:
                        string = field.field_id.field_description
                        value = getattr(datas, field.field_id.name)

                    if not value:
                        continue

                    if isinstance(value, dict):
                        model_obj = self.env[value._name]
                        value = eval("obj." + model_obj._rec_name,
                                     {'obj': value})

                    if not value:
                        value = ''

                    if field.nolabel:
                        string = ''
                    else:
                        string += ' :- '

                    if field.type == 'image' or field.type == 'barcode':
                        string = ''
                        if field.position != 'bottom':
                            pos = 'float:' + str(field.position) + ';'
                            bot = False
                        else:
                            bot = True
                            bot_dict = {'string': string, 'value': value,
                                        'type': field.type,
                                        'newline': field.newline,
                                        'style': "font-size:" +
                                        str(field.fontsize) + "px;" + pos}
                    else:
                        bot = False
                    if not bot:
                        vals_dict = {'string': string, 'value': value,
                                     'type': field.type,
                                     'newline': field.newline,
                                     'style': "font-size:" +
                                     str(field.fontsize) + "px;" + pos}
                        vals.append(vals_dict)
                if bot_dict != {}:
                    vals.append(bot_dict)
                if vals and vals[0]['value'] not in value_vals:
                    value_vals.append(vals[0]['value'])
                result.append(vals)
                temp = vals

        newlist_len = 0
        new_list = []
        result1 = []
        list_newdata = []
        for row in range(0, len(result) // (columns) + 1):
            val = result[row * columns: row * columns + columns]
            if val:
                new_list.append(val)
            for value_list in val:
                for value_print in value_list:
                    list_newdata.append(value_print['value'])

        for data in new_list:
            for list_data in data:
                newlist_len = newlist_len + 1

        remain_data = []
        counter = 0
        for newlist_data in list_newdata:
            if newlist_data in list_newdata:
                counter = counter + 1
            if counter > number_of_copy:
                counter = 1
            if counter < number_of_copy:
                remain_copy = number_of_copy - counter
                for xx in range(0, remain_copy):
                    remain_data.append(newlist_data)

        for data_value_vals in value_vals:
            if data_value_vals not in list_newdata:
                for add_data in range(0, number_of_copy):
                    remain_data.append(data_value_vals)

        if newlist_len <= number_of_copy:
            diff = number_of_copy - newlist_len

        if len(ids) == 1:
            for new_result in range(0, diff):
                result1.append(temp)

        return new_list

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form') or not self.env.context.get('active_model'):
            raise UserError(_("Form content is missing, \
                        this report cannot be printed."))

        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].\
            browse(self.env.context.get('active_ids', []))
        return {
            'doc_ids': docs.ids,
            'doc_model': self.model,
            'data': data,
            'docs': docs,
            'time': time,
            'get_data': self.get_data,
        }
