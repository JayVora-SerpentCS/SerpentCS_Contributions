# See LICENSE file for full copyright and licensing details.

{
    'name': 'Web Digital Signature v12.0',
    'version': '12.0.1.0.0',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'complexity': 'easy',
    'depends': ['web'],
    "license": "AGPL-3",
    'category': 'Tools',
    'description': '''
     This module provides the functionality to store digital signature
     Example can be seen into the User's form view where we have
        added a test field under signature.
    ''',
    'summary': '''
        Touch screen enable so user can add signature with touch devices.
        Digital signature can be very usefull for documents.
    ''',
    'images': ['static/description/Digital_Signature.jpg'],
    'data': [
        'views/web_digital_sign_view.xml',
        'views/users_view.xml'],
    'website': 'http://www.serpentcs.com',
    'qweb': ['static/src/xml/digital_sign.xml'],
    'installable': True,
    'auto_install': False,
}
