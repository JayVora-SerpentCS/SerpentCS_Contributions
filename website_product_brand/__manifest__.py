# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Product Brand Filtering in Website',
    'category': 'Website',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'http://www.serpentcs.com',
    'summary': '',
    'version': '10.0.0.0.1',
    'description': """
    Allows to use product brands as filtering for products in website.\n
    This Module depends on product_brand module
    -https://github.com/OCA/product-attribute/tree/10.0/product_brand
        """,
    'depends': ['product_brand', 'website_sale'],
    'data': [
        "security/ir.model.access.csv",
        "views/product_brand.xml",
    ],
    'installable': True,
    'auto_install': False,
}
