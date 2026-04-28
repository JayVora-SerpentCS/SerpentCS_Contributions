# See LICENSE file for full copyright and licensing details.

{
    'name': 'Hide Price and Discount in Quotation Report',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'category': 'Sales Management',
    'website': 'https://www.serpentcs.com',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'summary': 'Hide price/discount in Sale Order Report',
    'depends': ['sale_management'],
    'images': ['static/description/hide_price_and_discount_in_quotation_report_10.png'],
    'data': [
        'wizard/sale_wizard.xml',
        'security/ir.model.access.csv',
        'views/report_saleorder.xml',
    ],
    'price': '15',
    'currency': 'EUR',
    'installable': True,
}
