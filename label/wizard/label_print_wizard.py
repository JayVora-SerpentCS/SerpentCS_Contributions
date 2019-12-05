# See LICENSE file for full copyright and licensing details.

# 1: imports of python lib
import math

# 2:  imports of openerp
from odoo import fields, models, api
from odoo.tools import misc


class LabelPrintWizard(models.TransientModel):
    _name = 'label.print.wizard'

    @api.model
    def default_get(self, fields):
        if self._context is None:
            self._context = {}
        result = super(LabelPrintWizard, self).default_get(fields)
        if self._context.get('label_print'):
            label_print_obj = self.env['label.print']
            label_print_data = label_print_obj.browse(
                self._context.get('label_print'))
            for field in label_print_data.field_ids:
                if field.type == 'image':
                    result['is_image'] = True
                if field.type == 'barcode':
                    result['is_barcode'] = True
        return result

    name = fields.Many2one('label.config', 'Label Size', required=True)
    number_of_copy = fields.Integer('Number Of Copy', required=True, default=1)
    image_width = fields.Float('Width', default=50)
    image_height = fields.Float('Height', default=50)
    barcode_width = fields.Float('Width', default=50)
    barcode_height = fields.Float('Height', default=50)
    is_barcode = fields.Boolean('Is Barcode?')
    is_image = fields.Boolean('Is Image?')
    brand_id = fields.Many2one('label.brand', 'Brand Name', required=True)

    def print_report(self):
        if self._context is None:
            self._context = {}
        if not self._context.get('label_print') or not \
                self._context.get('active_ids'):
            return False
        total_record = len(self._context.get('active_ids', []))
        datas = {}
        for data in self.browse(self.ids):
            column = float(210) / float(data.name.width or 1)
            total_row = math.ceil(float(total_record) / (column or 1))
            no_row_per_page = int(297 / data.name.height)
            height = 297 / (no_row_per_page or 1)
            datas = {
                'rows': int(total_row),
                'columns': int(column) == 0 and 1 or int(column),
                'model': self._context.get('active_model'),
                'height': str(height * 3.693602694) + "mm",
                'no_row_per_page': no_row_per_page,
                'width': str(float(data.name.width) * 3.693602694) + "mm",
                'image_width': str(data.image_width),
                'image_height': str(data.image_height),
                'barcode_width': data.barcode_width,
                'barcode_height': data.barcode_height,
                'font_size': 10,
                'number_of_copy': data.number_of_copy,
                'top_margin': str(data.name.top_margin) + "mm",
                'bottom_margin': str(data.name.bottom_margin) + "mm",
                'left_margin': str(data.name.left_margin) + "mm",
                'right_margin': str(data.name.right_margin) + "mm",
                'cell_spacing': str(data.name.cell_spacing) + "px",
                'ids': self._context.get('active_ids', [])
            }
        cr, uid, context, su = self.env.args
        context = dict(context)
        context.update({"label_print_id": self._context.get('label_print'),
                        'datas': datas})
        self.env.args = cr, uid, misc.frozendict(context)

        data = {
            'ids': self.ids,
            'model': 'label.config',
            'form': datas
        }
        return self.env.ref('label.dynamic_label').with_context(context).\
            report_action(self, data=data)
