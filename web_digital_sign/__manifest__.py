# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
{
    "name": "Web Digital Signature v10.0",
    "version": "1.0",
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "category": '',
    'complexity': "easy",
    'depends': ['web'],
    "description": """
        This module provides the functionality to store digital signature
	image for a record.
        The example can be seen into the User's form view where we have added
	a test field under signature.
    """,
    'data': [
        'views/we_digital_sign_view.xml',
        'views/users_view.xml'
    ],
    'website': 'http://www.serpentcs.com',
    'qweb': ['static/src/xml/digital_sign.xml'],
    'installable': True,
    'auto_install': False,
}
