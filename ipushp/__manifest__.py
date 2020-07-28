# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{
    'name': 'iPushp - Employee Business Directory',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'category': 'Human Resource',
    'website': "http://www.serpentcs.com",
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'description': "iPushp - Employee Business Directory",
    'depends': ['hr', 'website'],
    'demo': [
        'data/ipushp_demo.xml',
    ],
    'data': [
        'security/ipushp_security.xml',
        'security/ir.model.access.csv',
        'data/website_data.xml',
        'views/assets.xml',
        'views/ipushp_config_view.xml',
        'views/hr_employee_view.xml',
        'views/website_ipushp_template.xml',
    ],
    'images': ['static/description/page_1.png'],
    'installable': True,
    'auto_install': False
}
