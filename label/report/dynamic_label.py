# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

# 1:  imports of openerp
from openerp.osv import osv
from openerp.report import report_sxw
from openerp.osv.orm import browse_record

# 2: imports of python lib
import barcode
from barcode.writer import ImageWriter
import base64
import logging

_logger = logging.getLogger(__name__)

# 3: local imports
try:
    import utils
    assert utils
except (ImportError, AssertionError):
    _logger.info('utils module not available. Please install "utils"\
                      python package.')

try:
    import cairosvg
    assert cairosvg
except (ImportError, AssertionError):
    _logger.info('cairosvg module not available. Please install "cairosvg"\
                      python package.')

import tempfile


class report_dynamic_label(report_sxw.rml_parse):
    
    def get_data(self,row,columns,ids,model,number_of_copy):
        active_model_obj = self.pool.get(model)
        label_print_obj = self.pool.get('label.print')
        label_print_data = label_print_obj.browse(self.cr, self.uid,
                                                  self.context.get('label_print'))
        result = []
        value_vals = []
        for datas in active_model_obj.browse(self.cr, self.uid, ids):
            for i in range(0, number_of_copy):
                vals=[]
                bot = False
                bot_dict={}
                for field in label_print_data.field_ids:
                    pos=''
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
                        value = eval("obj." + model_obj._rec_name, {'obj': value})
                        
                    if not value:
                        value = ''
                        
                    if field.nolabel:
                        string='';
                    else :
                        string+=' :- '
                        
                    if field.type == 'image' or field.type == 'barcode':
                        string = '';
                        if field.position != 'bottom':
                            pos ='float:'+ str(field.position)+';'
                            bot = False
                        else :
                            bot =True
                            bot_dict = {'string': string, 'value':  value,
                                        'type': field.type,
                                        'newline': field.newline,
                                        'style': "font-size:"+str(field.fontsize)+"px;"+pos}
                    else:
                        bot = False
                    if not bot:
                        vals_dict = {'string': string, 'value':  value,
                                     'type': field.type,
                                     'newline': field.newline,
                                     'style': "font-size:"+str(field.fontsize)+"px;"+pos}
                        vals.append(vals_dict)
                if bot_dict != {}:
                    vals.append(bot_dict)
                if vals[0]['value'] not in value_vals:
                    value_vals.append(vals[0]['value'])
                result.append(vals)
                temp = vals
                
        newlist_len = 0        
        new_list = []
        result1 = []
        list_newdata=[]
        for row in range(0,len(result)/(columns +1)):
            val = result[row*columns: row*columns + columns]
            if val:
                new_list.append(val)
            for value_list in val:
                for value_print in value_list:
                    list_newdata.append(value_print['value'])
                    
        for data in new_list:
            for list_data in data:
                newlist_len =newlist_len + 1
                
        remain_data = []
        counter = 0
        for newlist_data in list_newdata:
                if  newlist_data in list_newdata:
                    counter = counter + 1
                if counter > number_of_copy:
                    counter = 1
                if counter < number_of_copy:
                    remain_copy = number_of_copy - counter
                    for xx in range(0,remain_copy):
                        remain_data.append( newlist_data)
        
        for data_value_vals in value_vals:
            if data_value_vals not in list_newdata:
                 for add_data in range(0,number_of_copy):
                     remain_data.append(data_value_vals)
                 
        if newlist_len < number_of_copy:
            diff = number_of_copy - newlist_len
        
        new_val = []
        list_newdata=[]
        if len(ids) == 1:     
            for new_result in range(0, diff):
                    result1.append(temp)

        if len(ids) > 1:
                for remain_data_value in remain_data:
                    temp[0]['value']=remain_data_value
                    result1.append([temp[0].copy()])
                    
        for row in range(0, len(result1)):
                    new_val = result1[row*columns: row*columns + columns]
                    new_list.append(new_val)
        return new_list
         
    def __init__(self, cr, uid, name, context):
        
        super(report_dynamic_label,self).__init__(cr, uid, name, context=context)
        self.context=context
        self.rec_no = 0
        self.localcontext.update({
            'get_data':self.get_data,
        })

class report_employee(osv.AbstractModel):
    _name = 'report.label.report_label'
    _inherit = 'report.abstract_report'
    _template = 'label.report_label'
    _wrapped_report_class = report_dynamic_label
