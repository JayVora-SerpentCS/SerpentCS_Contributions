# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.multi
    @api.depends('product_variant_ids.sales_amt')
    def _sales_amt(self):
        for product in self:
            product.sales_amt = sum([p.sales_amt
                               for p in product.product_variant_ids])

    sales_amt = fields.Float(compute='_sales_amt', string='Sales amt')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def _sales_amt(self):
        res = {}
        amt = 0.00
        domain = [
            ('order_id.state', 'in', ['sale', 'done']),
            ('product_id', 'in', self.ids),
        ]
        order_lines = self.env['sale.order.line'].search(domain)
        for line in order_lines:
            amt += line.price_subtotal
            res[line.product_id.id] = {'amt': amt}
        for product in self:
            if res:
                product.sales_amt = res.get(product.id, 0).get('amt', 0)

    sales_amt = fields.Float(compute='_sales_amt', string='# Sales amt')
