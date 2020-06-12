# See LICENSE file for full copyright and licensing details.

{
    'name': 'Product Brand Filtering in Website',
    'category': 'Website',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'http://www.serpentcs.com',
    'license': 'LGPL-3',
    'summary': 'Product Brand based filters',
    'version': '12.0.0.1.0',
    'depends': ['product_brand', 'website_sale'],
    'data': [
        "security/ir.model.access.csv",
        "views/product_brand.xml",
    ],
    'installable': True,
    'auto_install': False,
}
