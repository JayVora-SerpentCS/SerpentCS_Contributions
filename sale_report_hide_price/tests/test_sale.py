# See LICENSE file for full copyright and licensing details.

from odoo.tests import common


class SaleOrderTest(common.TransactionCase):
    def setup(self):
        return super(SaleOrderTest, self).setup()

    def test_saleorder_action(self):
        self.sale_order = self.env["sale.order"]
        self.partner = self.env.ref("base.res_partner_2")
        service_delivery = self.env['product.product'].create({
            'name': 'Cost-plus Contract',
            'categ_id': self.env.ref('product.product_category_5').id,
            'standard_price': 200.0,
            'list_price': 180.0,
            'type': 'service',
            'uom_id': self.env.ref('uom.product_uom_unit').id,
            'uom_po_id': self.env.ref('uom.product_uom_unit').id,
            'default_code': 'SERV_DEL',
            'invoice_policy': 'delivery',
        })
        service_order_01 = self.env['product.product'].create({
            'name': 'Remodeling Service',
            'categ_id': self.env.ref('product.product_category_3').id,
            'standard_price': 40.0,
            'list_price': 90.0,
            'type': 'service',
            'uom_id': self.env.ref('uom.product_uom_hour').id,
            'uom_po_id': self.env.ref('uom.product_uom_hour').id,
            'description': 'Example of product to invoice on order',
            'default_code': 'PRE-PAID',
            'invoice_policy': 'order',
        })

        self.products = {
            "serv_order": service_order_01,
            "serv_deli": service_delivery,
        }

        self.order_idA = self.sale_order.create(
            {
                "partner_id": self.partner.id,
                "show_price": True,
                "show_discount": True,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": p.name,
                            "product_id": p.id,
                            "product_uom_qty": 2,
                            "product_uom": p.uom_id.id,
                            "price_unit": p.list_price,
                        },
                    )
                    for (_, p) in self.products.items()
                ],
            }
        )
