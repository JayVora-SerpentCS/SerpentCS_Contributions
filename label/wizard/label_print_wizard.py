# -*- coding: utf-8 -*-

from osv import osv
from osv import fields
import math

class label_print_wizard(osv.osv_memory):

    _name = 'label.print.wizard'

    def default_get(self, cr, uid, fields, context=None):
        if context is None:
            context = {}
        result = super(label_print_wizard, self).default_get(cr, uid, fields, context)
        if context.get('label_print'):
            label_print_obj = self.pool.get('label.print')
            label_print_data = label_print_obj.browse(cr, uid, context.get('label_print'), context)
            for field in label_print_data.field_ids:
                if field.type == 'image':
                    result['is_image'] = True
                if field.type == 'barcode':
                    result['is_barcode'] = True
        return result

    _columns = {
        'name' : fields.many2one('label.config','Label Size', required=True),
        'number_of_copy': fields.integer('Number Of Copy', required=True),
        'image_width': fields.float('Width'),
        'image_height': fields.float('Height'),
        'barcode_width': fields.float('Width'),
        'barcode_height': fields.float('Height'),
        'is_barcode': fields.boolean('Is Barcode?'),
        'is_image': fields.boolean('Is Image?'),
        'brand_id' : fields.many2one('label.brand', 'Brand Name', required=True)
    }

    _defaults = {
        'number_of_copy': 1,
        'image_width': 50,
        'image_height': 50,
        'barcode_width': 50,
        'barcode_height': 50,
    }
    
    def print_report(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if not context.get('label_print') or not context.get('active_ids'):
            return False
        total_record = len(context.get('active_ids', []))
        datas = {}
        for data in self.browse(cr, uid, ids, context):
            column = float(210) / float(data.name.width or 1)
            total_record = total_record * data.number_of_copy
            total_row = math.ceil(float(total_record)/ (column or 1))
            no_row_per_page = int(297 / data.name.height)
            height = 297 / (no_row_per_page or 1)
            datas = {
                'rows': int(total_row),
                'columns': int(column),
                'model' : context.get('active_model'),
                'height' : str(height * 3.693602694) + "px",
                'no_row_per_page': no_row_per_page,
                'width' : str(float(data.name.width)  * 3.693602694) + "px",
                'image_width': data.image_width,
                'image_height': data.image_height,
                'barcode_width': data.barcode_width,
                'barcode_height': data.barcode_height,
                'font_size' : 10,
                'number_of_copy': data.number_of_copy,
                'top_margin' : data.name.top_margin,
                'bottom_margin' : data.name.bottom_margin,
                'left_margin' : data.name.left_margin,
                'right_margin' : data.name.right_margin,
                'cell_spacing' : data.name.cell_spacing,
                'ids': context.get('active_ids', [])
            }
        context.update({"label_print_id":context.get('label_print'), 'datas': datas});
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'dynamic.label',
            'datas':datas,
            'context' : context,
        }

label_print_wizard()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
