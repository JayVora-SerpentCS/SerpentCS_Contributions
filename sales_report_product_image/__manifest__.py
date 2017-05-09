# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Product Image for Sale',
    'author': 'Serpent Consulting Services Pvt. Ltd.,\
             Odoo Community Association (OCA)',
    'category': 'Sales Management',
    'summary': 'Product Image for Sale Reports',
    'website': 'http://www.serpentcs.com',
    'version': '9.0.1.0.0',
    'sequence': 1,
    'depends': ['sale', 'web_tree_image'],
    'data': [
        'views/sale_product_view.xml',
        'views/report_saleorder.xml',
    ],
    'installable': True,
}
