# -*- coding: utf-8 -*-

from openerp import fields, models, api, _
from openerp.tools import misc


class label_print_wizard(models.TransientModel):

    _name = 'label.print.wizard'

    @api.model
    def default_get(self, fields):
        if self._context is None:
            self._context = {}
        result = super(label_print_wizard, self).default_get(fields)
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

    name = fields.Many2one('label.config', _('Label Type'), required=True)
    number_of_labels = fields.Integer(_('Number of Labels (per item)'),
                                      required=True,
                                      default=33)
    image_width = fields.Float(_('Width'), default=50)
    image_height = fields.Float(_('Height'), default=50)
    barcode_width = fields.Float(_('Width'), default=50)
    barcode_height = fields.Float(_('Height'), default=50)
    is_barcode = fields.Boolean(_('Is Barcode?'))
    is_image = fields.Boolean(_('Is Image?'))
    brand_id = fields.Many2one('label.brand', _('Brand Name'), required=True)

    @api.multi
    def print_report(self):
        if self._context is None:
            self._context = {}
        if (not self._context.get('label_print') or
                not self._context.get('active_ids')):
            return False
        datas = {}
        column = (float(210) / float(self.name.width or 1))
        no_row_per_page = int((297-self.name.left_margin -
                               self.name.right_margin) /
                              (self.name.height or 1))

        label_print_obj = self.env['label.print']
        label_print_data = label_print_obj.browse(
            self._context.get('label_print'))

        datas = {
            'rows': int(no_row_per_page),
            'columns': int(column),
            'model': self._context.get('active_model'),
            'height': self.name.height,
            'width': self.name.width,
            'image_width': self.image_width,
            'image_height': self.image_height,
            'barcode_width': self.barcode_width,
            'barcode_height': self.barcode_height,
            'number_of_labels': self.number_of_labels,
            'top_margin': self.name.top_margin,
            'bottom_margin': self.name.bottom_margin,
            'left_margin': self.name.left_margin,
            'right_margin': self.name.right_margin,
            'cell_spacing': self.name.cell_spacing,
            'ids': self.env.context['active_ids'],
            'padding_top': label_print_data.padding_top,
            'padding_bottom': label_print_data.padding_bottom,
            'padding_left': label_print_data.padding_left,
            'padding_right': label_print_data.padding_right,
        }

        cr, uid, context = self.env.args
        context = dict(context)
        context.update({"label_print_id": self.env.context['label_print'],
                        'datas': datas})
        self.env.args = cr, uid, misc.frozendict(context)

        data = {
            'ids': self.ids,
            'model': 'label.config',
            'form': datas
        }
        report_obj = self.env['report'].with_context(datas)
        return report_obj.get_action(self, 'label.report_label',
                                     data=data)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
