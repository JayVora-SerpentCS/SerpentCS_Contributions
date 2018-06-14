# See LICENSE file for full copyright and licensing details.

from odoo.tests import common


class WidgetMultiImageTest(common.TransactionCase):
    def setUp(self):
        super(WidgetMultiImageTest, self).setUp()

    def test_widgetmultiimage_action(self):
        self.category = self.env['product.category']
        self.categoryA = self.category.\
            create({'name': 'My category',
                    'property_valuation': 'manual_periodic'})

        self.product = self.env['product.template']
        self.productA = self.product.create({
            'name': 'Test Product PC',
            'categ_id': self.categoryA.id,
            'multi_images': [
                (0, 0, {'title': 'Product PC image1',
                        'image': 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8'}),
                (0, 0, {'title': 'Product PC image1',
                        'image': 'iVBORw0KGgoAAAANSUhEUgAAAB4AAAAbCAYAAABr/SR'
                        })]})
