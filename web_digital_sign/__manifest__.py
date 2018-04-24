# See LICENSE file for full copyright and licensing details.

{
    'name': 'Web Digital Signature v11.0',
    'version': '11.0.1.0.0',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'complexity': 'easy',
    'depends': ['web'],
    "license": "AGPL-3",
    'summary': 'Digital signature control',
    'images': ['static/description/Digital_Signature.jpg'],
    'data': [
        'views/we_digital_sign_view.xml',
        'views/users_view.xml'],
    'website': 'http://www.serpentcs.com',
    'qweb': ['static/src/xml/digital_sign.xml'],
    'installable': True,
    'auto_install': False,
}
