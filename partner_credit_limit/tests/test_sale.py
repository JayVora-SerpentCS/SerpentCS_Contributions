# -*- coding: utf-8 -*-
# Copyright 2016 Serpent Consulting Services Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo.tests import common


class TestSaleTestCase(common.TransactionCase):
    def setup(self):
        super(TestSaleTestCase, self).setup()

    def test_sale(self):
        self.respartner_obj = self.env['res.partner']
        self.partner = self.respartner_obj.\
            create({'name': 'Partner Name',
                    'over_credit': 'credit for Customer'})
        self.sale_obj = self.env['sale.order']
        self.record = self.sale_obj.\
            create({'partner_id': self.partner.id})
        self.record.action_confirm()
