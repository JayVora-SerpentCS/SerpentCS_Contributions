# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'SO - Product Price Check',
    'version': '10.0.1.0.0',
    'category': 'Sales Management',
    'summary': 'Restrict sales on 0 value.',
    'description': """
        This module restricts a user from confirming a Sale Order/Quotation
        if it contains products having sale price zero.
    """,
    'license': 'AGPL-3',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'http://www.serpentcs.com',
    'depends': ['sale'],
    'images': ['static/description/PriceCheck.png'],
    'installable': True,
    'auto_install': False,
}
