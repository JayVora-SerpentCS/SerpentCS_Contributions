# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "SO - Product Price Check",
    'version': '10.0.1.0.0',
    'category': 'Sales Management',
    'description': """
        This module restricts a user from confirming a Sale Order/Quotation
        if it contains products having sale price zero.
    """,
    'license': 'AGPL-3',
    'author': "Serpent Consulting Services Pvt. Ltd.",
    'website': 'http://www.serpentcs.com,'
               'Odoo Community Association (OCA)',
    'depends': ['sale'],
    'installable': True,
    'auto_install': False,
}
