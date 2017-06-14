# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
{
    'name': 'Web Security Dialog 10.0',
    'version': '10.0.1.0.0',
    'category': 'Web',
    'summary': 'Web Security Dialog',
    'description': """ """,
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'http://www.serpentcs.com',
    'depends': ['base','web'],
    'data': [
        'views/res_users_security.xml',
        'views/templates.xml'
    ],
    'qweb': ['static/src/xml/web_security_dialog.xml'],
    'auto_install': False,
    'installable': True,
    'application': True,
}

