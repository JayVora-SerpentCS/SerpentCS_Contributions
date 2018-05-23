# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class product_template(models.Model):
    _inherit = 'product.template'

    @api.multi
    @api.depends('product_variant_ids.invoice_count', 'product_variant_ids.invoice_amt')
    def _invoice_count(self):
        ''' Calculate invoice Amount and Qty. '''
        for product in self:
            product.invoice_count = sum([p.invoice_count for p in product.product_variant_ids])
            product.invoice_amt = sum([p.invoice_amt for p in product.product_variant_ids])

    @api.multi
    def action_view_invoice_qty(self):
        ''' Method add action for smart button '''
        self.ensure_one()
        action = self.env.ref('invoice_product_smart_buttons.action_product_invoice_list')
        product_ids = self.with_context(active_test=False).product_variant_ids.ids

        return {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'view_type': action.view_type,
            'view_mode': action.view_mode,
            'target': action.target,
            'context': "{'default_product_id': " + str(product_ids[0]) + "}",
            'res_model': action.res_model,
            'domain': [('invoice_id.state', 'in', ['open', 'paid']), ('product_id.product_tmpl_id', '=', self.id)],
        }

    invoice_count = fields.Integer(compute='_invoice_count', string='# Invoice qty')
    invoice_amt = fields.Float(compute='_invoice_count', string='# Invoice amt')

class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def _invoice_qty_amt_cal(self):
        '''
            Method calculate invoiced qty and amount for product
        '''
        res = {}
        qty = 0
        amt = 0.00
        domain = [
            ('invoice_id.state', 'in', ['open', 'paid']),
            ('invoice_id.type', 'in', ('out_invoice', 'out_refund')),
            ('product_id', 'in', self.ids),
        ]
        inv_lines = self.env['account.invoice.line'].search(domain)
        for inv in inv_lines:
            qty += inv.quantity
            amt += inv.price_subtotal
            res[inv.product_id.id] = {'qty': qty,'amt': amt} 
        
        for product in self:
            if res:
                product.invoice_count = res.get(product.id, 0).get('qty', 0)
                product.invoice_amt = res.get(product.id, 0).get('amt', 0)
    
    invoice_count = fields.Integer(compute='_invoice_qty_amt_cal', string='# Invoice qty')
    invoice_amt = fields.Float(compute='_invoice_qty_amt_cal', string='# Invoice amt')