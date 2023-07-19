# See LICENSE file for full copyright and licensing details.

{
    'name': 'POS Security Dialog',
    'version': '14.0.1.0.0',
    'category': 'Web',
    'summary': 'POS Security Dialog',
    'description': """POS Security Dialog""",
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'license': 'AGPL-3',
    'website': 'https://www.serpentcs.com',
    'depends': ['point_of_sale', 'web_security_dialog'],
    'data': [
        'views/pos_config_view.xml',
        'views/templates.xml'
    ],
    'installable': True,
    'application': True
}
