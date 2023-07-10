# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    sales_amt = fields.Float(compute="_compute_sales_amt", string="Sales amt")

    @api.depends("product_variant_ids.sales_amt")
    def _compute_sales_amt(self):
        for product in self:
            product.sales_amt = sum(
                product.product_variant_ids.mapped("sales_amt"))

    def action_view_sales_total(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "sale.report_all_channels_sales_action")
        action['domain'] = [('product_tmpl_id', 'in', self.ids)]
        action['context'] = {
            'pivot_measures': ['price_total'],
            'active_id': self._context.get('active_id'),
            'search_default_Sales': 1,
            'active_model': 'sale.report',
            'search_default_filter_order_date': 1,
        }
        return action


class ProductProduct(models.Model):
    _inherit = "product.product"

    sales_amt = fields.Float(
        compute="_compute_sales_amt", string="# Sales amt")

    @api.depends("product_tmpl_id.sales_amt")
    def _compute_sales_amt(self):
        res = {}
        order_lines = self.env["sale.order.line"].search([
            ("order_id.state", "in", ["sale", "done"]),
            ("product_id", "in", self.ids),
        ])
        for line in order_lines:
            if res.get(line.product_id.id):
                res.get(line.product_id.id).update(
                    {
                        "amt": res.get(line.product_id.id).get("amt")
                        + line.price_subtotal
                    }
                )
            else:
                res[line.product_id.id] = {"amt": line.price_subtotal}

        for product in self:
            product.sales_amt = 0.0
            if res and res.get(product.id):
                product.sales_amt = res.get(product.id).get("amt", 0)
