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

from report import report_sxw
import barcode
from barcode.writer import ImageWriter
import base64
from osv.orm import browse_record
#import utils
import cairosvg
import cairo
import rsvg
import tempfile

class report_dynamic_label(report_sxw.rml_parse):

    def generate_barcode(self, barcode_string, height, width):
        temp_path_svg = tempfile.gettempdir()+"/temp_barcode"
        temp_path_png = tempfile.gettempdir()+"/temp_barcode.png"
        code39 = barcode.get_barcode_class('code39')
        c39 = code39(str(barcode_string))
        fullname = c39.save(temp_path_svg)
        file = open(temp_path_svg+".svg")
        
        img = cairo.ImageSurface(cairo.FORMAT_ARGB32, 200,75)
        ctx = cairo.Context(img)
        svg_data = file.read()
        handler = rsvg.Handle(None, str(svg_data))
        handler.render_cairo(ctx)
        img.write_to_png(temp_path_png)
        
        name = open(temp_path_png, "r+")
        barcode_data = base64.b64encode(name.read())
        return barcode_data
#         barcode_data = ""
#         try:
#             EAN = barcode.get_barcode_class('code39')
#             ean = EAN(barcode_string, writer=ImageWriter())
#             ean.default_writer_options['font_size'] = 1
#             ean.default_writer_options['text_distance'] = False
#             ean.default_writer_options['quiet_zone'] = 2.0
#             fullname = ean.save('code39_barcode')
#             name = open(fullname, "r+")
#             barcode_data = base64.b64encode(name.read())
#         except Exception, e:
#             return False
#         return barcode_data

#         try:
#             from reportlab.graphics.barcode import code128
#             from reportlab.graphics.barcode import code39
#             from reportlab.graphics.barcode import code93
#             from reportlab.graphics.barcode import common
#             from reportlab.graphics.barcode import fourstate
#             from reportlab.graphics.barcode import usps
#             from reportlab.graphics.barcode import createBarcodeDrawing
#         except ImportError:
#             _logger.warning("Cannot use barcode renderers:", exc_info=True)
#             return None
# #         args = utils.attr_get(node, [], {'ratio':'float','xdim':'unit','height':'unit','checksum':'int','quiet':'int','width':'unit','stop':'bool','bearers':'int','barWidth':'float','barHeight':'float'})
#         codes = {
#             'codabar': lambda x: common.Codabar(x, **args),
#             'code11': lambda x: common.Code11(x, **args),
#             'code128': lambda x: code128.Code128(str(x), **args),
#             'standard39': lambda x: code39.Standard39(str(x), **args),
#             'standard93': lambda x: code93.Standard93(str(x), **args),
#             'i2of5': lambda x: common.I2of5(x, **args),
#             'extended39': lambda x: code39.Extended39(str(x), **args),
#             'extended93': lambda x: code93.Extended93(str(x), **args),
#             'msi': lambda x: common.MSI(x, **args),
#             'fim': lambda x: usps.FIM(x, **args),
#             'postnet': lambda x: usps.POSTNET(x, **args),
#             'ean13': lambda x: createBarcodeDrawing('EAN13', value=str(x), **args),
#             'qrcode': lambda x: createBarcodeDrawing('QR', value=x, **args),
#         }
#         code = 'standard39'
# #         if node.get('code'):
# #             code = node.get('code').lower()
#         print "dgdsfgsdfgsdfg",codes[code](barcode_string)
#         return codes[code](barcode_string)

    def _get_record(self, rows, columns, ids, model, number_of_copy):
        active_model_obj = self.pool.get(model)
        label_print_obj = self.pool.get('label.print')
        label_print_data = label_print_obj.browse(self.cr, self.uid, self.context.get('label_print'))
        result = []
        
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
                            pos ='float:'+field.position+';'
                            bot = False
                        else :
                            bot =True
                            bot_dict = {'string': string, 'value':  value, 'type': field.type, 'newline': field.newline, 'style': "font-size:"+str(field.fontsize)+"px;"+pos}
                    else:
                        bot = False
                    if not bot:
                        vals_dict = {'string': string, 'value':  value, 'type': field.type, 'newline': field.newline, 'style': "font-size:"+str(field.fontsize)+"px;"+pos}
                        vals.append(vals_dict)
                if bot_dict != {}:
                    vals.append(bot_dict)
                result.append(vals)
        new_list = []
        for row in range(0, len(result)/(columns)):
            val = result[row*columns: row*columns + columns]
            if val:
                new_list.append(val)
        return new_list

    def __init__(self, cr, uid, name, context):
        super(report_dynamic_label,self).__init__(cr, uid, name, context=context)
        self.context=context
        self.rec_no = 0
        self.localcontext.update({
            'get_record' : self._get_record,
            'generate_barcode': self.generate_barcode
        })

report_sxw.report_sxw('report.dynamic.label','label.config','addons/label/report/dynamic_label.mako',parser=report_dynamic_label, header=False)

