# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Import / Export Templating',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'category': 'Base',
    'description': """
        This module features to export blank template based on ir.model fields.
        & provided .xls extension file to import!
    """,
    'summary': """
    Standard import export template
    USer friendly templates to upload download bulk data
    Manage easy import export for non-technical users of ERP
    """,
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'http://www.serpentcs.com',
    'depends': ['base', 'web'],
    'data': [
        'wizard/wiz_download_template_view.xml',
        'views/templates.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'price': 30.0,
    'currency': 'EUR',
}
