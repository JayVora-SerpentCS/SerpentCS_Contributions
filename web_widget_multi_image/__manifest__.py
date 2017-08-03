# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Web Widget Multi Image V10',
    'version': '10.0.0.0.1',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'category': 'Image',
    'complexity': 'easy',
    'depends': ['product'],
    'license': 'AGPL-3',
    'data': [
        'view/templates.xml',
        'view/product_view.xml',
    ],
    'website': 'http://www.serpentcs.com',
    'qweb': ['static/src/xml/image_multi.xml'],
    'installable': True,
    'auto_install': False,
}
