# See LICENSE file for full copyright and licensing details.

{
    'name': 'Web Widget Multiple Image V12',
    'version': '12.0.0.1.0',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'category': 'Image',
    'complexity': 'easy',
    'depends': ['product'],
    'license': 'AGPL-3',
    'summary': 'Multiple web images widget',
    'data': [
        'security/ir.model.access.csv',
        'view/templates.xml',
        'view/product_view.xml',
    ],
    'website': 'http://www.serpentcs.com',
    'qweb': ['static/src/xml/image_multi.xml'],
    'installable': True,
    'auto_install': False,
}
