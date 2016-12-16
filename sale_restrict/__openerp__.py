# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "SO - Product Price Check",
    'version': '9.0.1.1.0',
    'category': 'Sales Management',
    'description': """
        This module restricts a user from confirming a Sale Order/Quotation 
        if it contains products having sale price zero.
    """,
    'author': "Serpent Consulting Services Pvt. Ltd.",
    'website': "http://www.serpentcs.com",
    'depends': ['sale'],
    'installable': True,
    'auto_install': False,
}
