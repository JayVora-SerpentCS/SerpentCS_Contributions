# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.depends("product_variant_ids.sales_amt")
    def _compute_sales_amt(self):
        for product in self:
            product.sales_amt = sum([p.sales_amt for p in product.product_variant_ids])

    sales_amt = fields.Float(compute="_compute_sales_amt", string="Sales amt")


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _compute_sales_amt(self):
        res = {}
        amt = 0.00
        sales_amount = 0.0
        domain = [
            ("order_id.state", "in", ["sale", "done"]),
            ("product_id", "in", self.ids),
        ]
        order_lines = self.env["sale.order.line"].search(domain)

        for line in order_lines:
            amt += line.price_subtotal
            res[line.product_id.id] = {"amt": amt}
        for product in self:
            if res:
                sales_amount = (
                    res[product.id].get("amt", 0.0) if product.id in res else 0.0
                )
        self.sales_amt = sales_amount

    sales_amt = fields.Float(compute="_compute_sales_amt", string="# Sales amt")
