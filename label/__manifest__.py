# See LICENSE file for full copyright and licensing details.
{
    "name": "Mass Label Reporting",
    "version": "13.0.1.0.0",
    "category": "Tools",
    "license": "AGPL-3",
    "summary": "Generate customised labels of any document",
    "author": 'Serpent Consulting Services Pvt. Ltd.',
    "website": "http://www.serpentcs.com",
    "maintainer": 'Serpent Consulting Services Pvt. Ltd.',
    'depends': ['base'],
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
    'uninstall_hook': 'uninstall_hook',
    'images': ['static/description/Label.png'],
    'installable': True,
    'auto_install': False,
}
