# See LICENSE file for full copyright and licensing details.

{
    'name': 'Hide Price and Discount in Quotation Report',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'category': 'Sales Management',
    'website': 'http://www.serpentcs.com',
    'version': '16.0.1.0.1',
    'license': 'LGPL-3',
    'summary': 'Hide price/discount in Sale Order Report',
    'depends': [
        'sale_management'
    ],
    'images': ['static/description/icon.png'],
    'data': [
        'views/sale_view.xml',
        'views/report_saleorder.xml',
        'views/preview_sale_order.xml'
    ],
    'installable': True,
}
