# See LICENSE file for full copyright and licensing details.

{
    'name': 'Sale Product Smart Buttons',
    'version': '13.0.0.0.1',
    'sequence': 1,
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'https://www.serpentcs.com',
    'description': """ Module will add Smart button to show
        Sale amount for particular product
        Smart button on Product
        Smart button for Amount Sale on product
        """,
    'summary': """Sale Product smart buttons.
        Smart button on Product
        Smart button for Amount sale on product
    """,
    'category': 'Products',
    'license': 'AGPL-3',
    'depends': ['sale_management'],
    'data': [
        'views/product_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 10,
    'currency': 'EUR'
}
