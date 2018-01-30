# See LICENSE file for full copyright and licensing details.
{
    'name': 'Web Widget Multiple Image V10',
    'version': '11.0.0.0.1',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'category': 'Image',
    'complexity': 'easy',
    'depends': ['product'],
    'license': 'AGPL-3',
    'summary': 'Multiple web images widget',
    'description': ''' Web widget to load and swap multiple images.''',
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
