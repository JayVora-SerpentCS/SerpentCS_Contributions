# See LICENSE file for full copyright and licensing details.

{
    'name': 'Product Brand Filtering in Website',
    'category': 'Website',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'http://www.serpentcs.com',
    'license': 'AGPL-3',
    'summary': 'Product Brand based filters',
    'version': '11.0.0.0.1',
    'depends': ['product_brand', 'website_sale'],
    'data': [
        "security/ir.model.access.csv",
        "views/product_brand.xml",
    ],
    'installable': False,
    'auto_install': False,
}
