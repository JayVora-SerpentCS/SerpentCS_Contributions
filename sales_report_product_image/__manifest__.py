# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Product Image for Sale',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'category': 'Sales Management',
    'summary': 'Product Image for Sale Reports',
    'license': 'AGPL-3',
    'website': 'http://www.serpentcs.com',
    'version': '10.0.1.0.0',
    'sequence': 1,
    'depends': ['sale', 'web_tree_image'],
    'data': [
        'views/sale_product_view.xml',
        'views/report_saleorder.xml',
    ],
    'installable': True,
}
