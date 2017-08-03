# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
{
    'name': 'Web Security Dialog 10.0',
    'version': '10.0.1.0.0',
    'category': 'Web',
    'summary': 'Web Security Dialog',
    'description': """
    This module provides the functionality to generalize security on
    any type of button.
    -> Offers company level security & restricted access.
    -> Configuring security code to buttons from company configuration
       menu.
    -> Enhances webpage security at the interface level.
    Passing the options and confirm attributes inside the button like below.
        -> <button name="method_name" type="object" string="create
        invoice" options='{"security":"security_field"}'/>""",
    'author': 'Serpent Consulting Services Pvt. Ltd.',
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
