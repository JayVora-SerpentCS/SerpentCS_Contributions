# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Record and Create Modules',
    'version': '9.0.1.0.0',
    'category': 'Tools',
    'description': """
This module allows you to create a new module without any development.
======================================================================

It records all operations on objects during the recording session and
produce a .ZIP module. So you can create your own module directly from
the OpenERP client.

This version works for creating and updating existing records. It recomputes
dependencies and links for all types of widgets (many2one, many2many, ...).
It also support workflows and demo/update data.

This should help you to easily create reusable and publishable modules
for custom configurations and demo/testing data.

How to use it:
Run Administration/Customization/Module Creation/Export Customizations As a Module wizard.
Select datetime criteria of recording and objects to be recorded and Record module.
    """,
    'author': 'OpenERP SA, Serpent Consulting Services Pvt. Ltd.',
    'website': 'http://www.openerp.com, http://www.serpentcs.com',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/base_module_record_object_view.xml',
        'wizard/base_module_record_data_view.xml',
    ],
    'installable': True,
    'auto_install':False,
    'images': ['images/base_module_record1.jpeg',
               'images/base_module_record2.jpeg',
               'images/base_module_record3.jpeg',]
}
