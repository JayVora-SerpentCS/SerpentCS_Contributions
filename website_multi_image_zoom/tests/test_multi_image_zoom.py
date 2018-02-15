# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and
# licensing details.http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class MultiImageZoomTest(common.TransactionCase):
    def setUp(self):
        super(MultiImageZoomTest, self).setUp()

    def test_multiimagezoom_action(self):
        self.category = self.env['product.category']
        self.categoryA = self.category.\
            create({'name': 'My category',
                    'property_valuation': 'manual_periodic'})

        self.product = self.env['product.product']
        self.productA = self.product.create({
            'name': 'Test Product PC',
            'type': 'product',
            'categ_id': self.categoryA.id,
            'images_variant': [
                (0, 0, {'name': 'Product PC image1',
                        'image': 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8'}),
                (0, 0, {'name': 'Product PC image1',
                        'image': 'iVBORw0KGgoAAAANSUhEUgAAAB4AAAAbCAYAAABr/SR'
                        })]})
