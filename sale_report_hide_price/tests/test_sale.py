# -*- coding: utf-8 -*-
# © 2016 Serpent Consulting Services Pvt. Ltd. <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class SaleOrderTest(common.TransactionCase):

    def setup(self):
        super(SaleOrderTest, self).setup()

    def test_saleorder_action(self):
        self.sale_order = self.env['sale.order']
        self.partner = self.env.ref('base.res_partner_2')
        self.products = {
            'serv_order': self.env.ref('product.service_order_01'),
            'serv_deli': self.env.ref('product.service_delivery'),
        }

        self.order_idA = self.sale_order.create({
            'partner_id': self.partner.id,
            'hide_price': True,
            'show_discount': True,
            'order_line': [
                (0, 0, {'name': p.name, 'product_id': p.id,
                        'product_uom_qty': 2, 'product_uom': p.uom_id.id,
                        'price_unit': p.list_price
                        })for (_, p) in self.products.iteritems()],
        })
