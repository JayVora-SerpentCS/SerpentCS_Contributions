# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Mass Label Reporting",
    "version": "10.0.1.0.0",
    "author": 'Serpent Consulting Services Pvt. Ltd.',
    "category": "Tools",
    "license": "AGPL-3",
    "website": "http://www.serpentcs.com",
    "description": """
    The video : https://www.youtube.com/watch?v=Fps5FWfcLwo
    """,
    'depends': ['report'],
    'data': [
        'data/report_paperformat.xml',
        'security/label.brand.csv',
        'security/label.config.csv',
        'security/ir.model.access.csv',
        'views/label_config_view.xml',
        'views/label_print_view.xml',
        'views/label_size_data.xml',
        'wizard/label_print_wizard_view.xml',
        'views/label_report.xml',
        'report/dynamic_label.xml'
    ],
    'images': ['static/description/Label.png'],
    'installable': True,
    'auto_install': False,
}
