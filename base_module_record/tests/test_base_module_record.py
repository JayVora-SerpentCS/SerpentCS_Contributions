# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
from odoo.tests import common
from datetime import datetime, timedelta


class BaseModuleRecordTestCase(common.TransactionCase):
    def setUp(self):
        super(BaseModuleRecordTestCase, self).setUp()

    def test_BaseModuleRecord_action(self):
        self.basemodule_obj = self.env['base.module.record']
        check_date = datetime.\
            strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                     "%Y-%m-%d %H:%M:%S")
        check_date += timedelta(days=-3)
        object_lst = []
        for o_id in self.basemodule_obj._get_default_objects():
            object_lst.append(o_id.id)
        self.basemodule_id = self.basemodule_obj.\
            create({'check_date': check_date,
                    'filter_cond': 'created',
                    'objects': [(6, 0, object_lst)]
                    })
        record = self.basemodule_id.record_objects()
        self.base_mod_rec_obj = self.env[record['res_model']]
        self.base_mod_rec_obj_id = self.base_mod_rec_obj.\
            create({'name': 'Modules',
                    'directory_name': 'Module Director',
                    'version': '1.0',
                    'author': 'Serpentcs',
                    'category': 'Vertical Modules/Parametrization',
                    'website': 'https://www.odoo.com',
                    'description': 'Module Recording',
                    'data_kind': 'demo'})
        self.base_mod_rec_obj.inter_call([self.base_mod_rec_obj_id.id])


class BaseModuleDataTestCase(common.TransactionCase):
    def setUp(self):
        super(BaseModuleDataTestCase, self).setUp()

    def test_BaseModuleData_action(self):
        self.basemoduledata_obj = self.env['base.module.data']
        check_date = datetime.\
            strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                     "%Y-%m-%d %H:%M:%S")
        check_date += timedelta(days=-3)
        object_lst = []
        for o_id in self.basemoduledata_obj._get_default_objects():
            object_lst.append(o_id.id)
        self.basemoduledata_id = self.basemoduledata_obj.\
            create({'check_date': check_date,
                    'filter_cond': 'created',
                    'objects': [(6, 0, object_lst)]
                    })
        self.basemoduledata_id.record_objects()
