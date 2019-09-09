# See LICENSE file for full copyright and licensing details.

{
    'name': 'Product Image for Sale',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'version': '13.0.1.0.0',
    'category': 'Sales Management',
    'summary': 'Product Image for Sale Reports',
    'license': 'AGPL-3',
    'website': 'http://www.serpentcs.com',
    'depends': [
        'sale',
        'web_tree_image', #OCA should have it in v12
    ],
    'data': [
        'views/sale_product_view.xml',
        'views/report_saleorder.xml',
    ],
    'installable': True,
}
