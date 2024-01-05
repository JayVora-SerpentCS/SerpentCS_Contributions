# See LICENSE file for full copyright and licensing details.

{
    'name': 'Import / Export Templating',
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'http://www.serpentcs.com',
    'category': 'Base',
    'summary': """
    Standard import export template,
    User-friendly templates to upload download bulk data Manage easy
    import-export for non-technical users of ERP.
    """,
    'depends': ['web'],
    'data': [
        'wizard/wiz_download_template_view.xml',
        'views/templates.xml',
    ],
    'installable': True,
    'price': 30.0,
    'currency': 'EUR',
}
