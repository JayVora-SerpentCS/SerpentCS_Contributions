# -*- coding: utf-8 -*-
# Copyright 2016 Serpent Consulting Services Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo.tests import common


class SaleReportProductImageTestCase(common.TransactionCase):

    def setup(self):
        super(SaleReportProductImageTestCase, self).setup()

    def test_sale_report_product(self):

        self.product = self.env.ref('product.product_product_7')
        self.partner = self.env.ref('base.res_partner_2')

        self.env['sale.order'].create(
            {
                'partner_id': self.partner.id,
                'partner_invoice_id': self.partner.id,
                'partner_shipping_id': self.partner.id,
                'pricelist_id': self.env.ref('product.list0').id,
                'print_image': 'True',
                'image_sizes': 'image_medium',
                'image_small': self.product.image_small,
            })
