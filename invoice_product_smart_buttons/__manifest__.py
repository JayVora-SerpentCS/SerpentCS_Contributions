# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{

    'name': 'Invoice Product Smart Buttons',
    'version': '11.0.0.0.1',
    'sequence': 1,
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'https://www.serpentcs.com',
    'description': """ Module will add Smart button to show
        invoiced Qty and amount for particular product
        Smart button on Product
        Smart BI for Invoiced quantity of Product
        Smart button for Amount invoiced on product
        """,
    'summary': """Invoice Product smart buttons.
        Smart button on Product
        Smart BI for Invoiced quantity of Product
        Smart button for Amount invoiced on product
    """,
    'category': 'Products',
    'license': 'AGPL-3',
    'depends': ['account', 'sale_management'],
    'data': [
            'views/invoice_line_view.xml',
            'views/product_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 10,
    'currency': 'EUR'
}
