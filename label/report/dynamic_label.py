# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012 Serpent Consulting Services (<http://www.serpentcs.com>)
#    Copyright (C) 2004-2010 OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################
from openerp.osv import osv
from openerp.report import report_sxw
from openerp.osv.orm import browse_record

from copy import deepcopy
from math import ceil


class report_dynamic_label(report_sxw.rml_parse):
    def get_data(self, row, columns, ids, model, nber_labels):
        """
        TODO take into account sequence
        Function called in the xml in order to get the datas for one page
        (in dynamic_label.xml).
        If multiple ids are given, the labels will be grouped by ids (therefore
        N Bob, then N Will, ...).

        :param int row: Number of row for one page of labels
        :param int columns: Number of columns of labels
        :param ids: Id(s) of the model
        :param model: Model used for the labels
        :param int nber_labels: Number of labels of each ids

        :returns: Data to print
        :rtype: list[row,columns,value] = dict
        """
        active_model_obj = self.pool.get(model)
        label_print_obj = self.pool.get('label.print')
        label_print_data = label_print_obj.browse(
            self.cr, self.uid, self.context.get('label_print'))
        tot = nber_labels * len(ids)
        tot_rows = int(ceil(float(ceil(tot) / columns)))
        print row, columns, ids, model, nber_labels
        # return value
        result = [[None for i in range(columns)] for j in range(tot_rows-1)]
        result.append([None for i in range(tot_rows*columns-tot)])
        print result
        # current indices
        cur_row = 0
        cur_col = 0
        for id_model in ids:
            datas = active_model_obj.browse(self.cr, self.uid, id_model)
            # value to add
            vals = []
            bot = False
            bot_dict = []
            # loop over each field for one label
            for field in label_print_data.field_ids:
                pos = ''
                if field.python_expression and field.python_field:
                    string = field.python_field.split('.')[-1]
                    value = eval(field.python_field, {'obj': datas})

                elif field.field_id.name:
                    string = field.field_id.field_description
                    value = getattr(datas, field.field_id.name)

                if not value:
                    continue

                if isinstance(value, browse_record):
                    model_obj = self.pool.get(value._name)
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
                        pos = 'float:' + str(field.position)+';'
                        bot = False
                    else:
                        bot = True
                        bot_dict.appends({'string': string,
                                          'value':  value,
                                          'type': field.type,
                                          'newline': field.newline,
                                          'style': "font-size:" +
                                          str(field.fontsize)+"px;"+pos})
                else:
                    bot = False
                if not bot:
                    vals_dict = {'string': string,
                                 'value':  value,
                                 'type': field.type,
                                 'newline': field.newline,
                                 'style': "font-size:" +
                                 str(field.fontsize)+"px;"+pos}
                    vals.append(vals_dict)
            if len(bot_dict) > 0:
                vals.append(bot_dict)
            for i in range(nber_labels):
                result[cur_row][cur_col] = deepcopy(vals)
                cur_col += 1
                if cur_col >= columns:
                    cur_col = 0
                    cur_row += 1
        print result
        return result

    def __init__(self, cr, uid, name, context):
        super(report_dynamic_label, self).__init__(
            cr, uid, name, context=context)
        self.context = context
        self.rec_no = 0
        self.localcontext.update({
            'get_data': self.get_data,
        })


class report_employee(osv.AbstractModel):
    _name = 'report.label.report_label'
    _inherit = 'report.abstract_report'
    _template = 'label.report_label'
    _wrapped_report_class = report_dynamic_label
