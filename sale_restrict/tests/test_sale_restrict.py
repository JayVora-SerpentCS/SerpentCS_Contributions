# See LICENSE file for full copyright and licensing details.

from odoo.tests import common


class SaleOrder(common.TransactionCase):

    def setup(self):
        super(SaleOrder, self).setup()

    def test_sale_action(self):
        self.partner = self.ref('base.res_partner_2')
        self.product_1 = self.env.ref('product.product_product_12')
        self.sale_order = self.env['sale.order'].create(
            {'partner_id': self.partner,
             'order_line': [(0, 0, {'name': self.product_1.name,
                                    'product_id': self.product_1.id,
                                    'product_uom_qty': 2,
                                    'product_uom': self.product_1.uom_id.id,
                                    'price_unit': self.product_1.list_price}
                             )],
             })
        self.sale_order.action_confirm()
