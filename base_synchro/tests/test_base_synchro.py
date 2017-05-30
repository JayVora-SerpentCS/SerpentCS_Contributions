# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
from odoo.tests import common


class BaseSynchroObjTestCase(common.TransactionCase):
    def setUp(self):
        super(BaseSynchroObjTestCase, self).setUp()

        self.server_model = self.env['base.synchro.server']
        self.server = self.server_model.\
            create({
                'name': 'Test Server',
                'server_url': '127.0.0.1',
                'server_port': '8069',
                'server_db': 'base_test',
                'login': 'a',
                'password': 'a',
                })

    def test_BaseSynchroObj_action(self):
        self.basesyncro_obj = self.env['base.synchro.obj'].\
            create({'name': 'Test base syncro',
                    'domain': '[]',
                    'server_id': self.server.id,
                    'model_id': 1,
                    'action': 'd',
                    })
        self.basesyncro.get_ids('base', '', [], {'action': 'u'})
        self.basesyncro._get_ids('base', '', [], {'action': 'u'})

    def test_basesynchro(self):
        self.basesyncro = self.env['base.synchro'].\
            create({'server_url': self.server.id})
