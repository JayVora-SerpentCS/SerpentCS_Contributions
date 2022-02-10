# See LICENSE file for full copyright and licensing details.

from odoo.tests import common


class SaleOrderTest(common.TransactionCase):

    def setup(self):
        super(SaleOrderTest, self).setup()

    def test_saleorder_action(self):
        self.sale_order_obj = self.env['sale.order']
        self.partner = self.env.ref('base.res_partner_2')
        self.products = {
            'serv_order': self.env.ref('product.product_delivery_01'),
            'serv_deli': self.env.ref('product.product_order_01'),
        }

        self.sale_order_id = self.sale_order_obj.create({
            'partner_id': self.partner.id,
            'show_price': True,
            'show_discount': True,
            'order_line': [
                (0, 0, {'name': product_1.name, 'product_id': product_1.id,
                        'product_uom_qty': 2, 'product_uom': product_1.uom_id.id,
                        'price_unit': product_1.list_price
                        }) for (_, product_1) in self.products.items()],
        })
