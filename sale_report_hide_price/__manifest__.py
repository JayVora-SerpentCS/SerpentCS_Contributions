# See LICENSE file for full copyright and licensing details.

{
    'name': 'Hide Price and Discount in Quotation Report',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'category': 'Sales Management',
    'website': 'https://www.serpentcs.com',
    'version': '17.0.1.0.1',
    'license': 'LGPL-3',
    'summary': 'Hide price/discount in Sale Order Report',
    'depends': ['sale_management'],
    'images': ['static/description/icon.png'],
    'data': [
        'wizard/sale_wizard.xml',
        'security/ir.model.access.csv',
        'views/report_saleorder.xml',
    ],
    'installable': True,
}
