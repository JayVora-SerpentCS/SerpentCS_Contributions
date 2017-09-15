# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Record and Create Modules',
    'version': '9.0.1.0.0',
    'category': 'Tools',
    'author': 'OpenERP SA, Serpent Consulting Services Pvt. Ltd.',
    'website': 'http://www.openerp.com, http://www.serpentcs.com',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/base_module_record_object_view.xml',
        'wizard/base_module_record_data_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'images': ['images/base_module_record1.jpeg',
               'images/base_module_record2.jpeg',
               'images/base_module_record3.jpeg']
}
