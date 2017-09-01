# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Product Brand Filtering in Website',
    'category': 'Website',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'http://www.serpentcs.com',
    'license': 'AGPL-3',
    'summary': 'Product Brand based filters',
    'version': '10.0.0.0.1',
    'depends': ['product_brand', 'website_sale'],
    'data': [
        "security/ir.model.access.csv",
        "views/product_brand.xml",
    ],
    'installable': True,
    'auto_install': False,
}
