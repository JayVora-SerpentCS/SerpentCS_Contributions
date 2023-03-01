from odoo import api, fields, models, _


class HidePriceReport(models.AbstractModel):
    """Report Sale Order model."""
    _name = 'report.sale.report_saleorder'
    _description = "Report Sale Order"

    @api.model
    def _get_report_values(self, docids, data=None):
        sale_order_obj = self.env['sale.order']
        context = dict(self._context) or {}
        order_ids = context.get('active_ids')
        show_price = data.get('show_price')
        show_discount = data.get('show_discount')
        docargs = {
            'doc_ids': docids,
            'doc_model': sale_order_obj,
            'data': data,
            'docs': sale_order_obj.browse(order_ids) if order_ids else sale_order_obj.browse(docids),
            'discount': show_discount,
            'price': show_price
        }

        return docargs
