# See LICENSE file for full copyright and licensing details.

from odoo.tests import common


class CityAreaTestCase(common.TransactionCase):
    def setUp(self):
        super(CityAreaTestCase, self).setUp()

    def test_cityarea_action(self):
        self.country_belgium = self.env['res.country'].\
            search([('code', 'like', 'BE')], limit=1)

        self.state_id = self.env['res.country.state'].\
            search([('country_id', '=', self.country_belgium.id)], limit=1)

        self.city = self.env['city.city'].\
            create({'name': 'Test City',
                    'state_id': self.state_id.id,
                    'zip': '12',
                    'country_id': self.country_belgium.id,
                    'code': 'TCT'})

        self.cityarea = self.env['city.area'].\
            create({'name': 'Test City Area',
                    'zip': '123545687',
                    'city_id': self.city.id,
                    'code': 'TCA'})

        self.res_partner = self.env['res.partner']
        self.test_res_part = self.res_partner.\
            create({'name': 'Test Partner',
                    'area_id': self.cityarea.id})
        self.test_res_part.onchange_area_id()
