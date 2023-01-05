# See LICENSE file for full copyright and licensing details.

{
    'name': 'Web Security Dialog 11.0',
    'version': '11.0.1.0.0',
    'category': 'Web',
    'summary': 'Web Security Dialog',
    'author': '''Serpent Consulting Services Pvt. Ltd.,
                Odoo Community Association (OCA)''',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'license': 'AGPL-3',
    'website': 'http://www.serpentcs.com',
    'depends': ['base', 'web'],
    'data': [
        'views/res_company_security.xml',
        'views/templates.xml'
    ],
    'qweb': ['static/src/xml/web_security_dialog.xml'],
    'images': ['static/description/web_banner.png'],
    'installable': True,
    'application': True
}
