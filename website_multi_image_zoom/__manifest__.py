# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Website Product Multi-Image Zoom',
    'category': 'Website',
    'summary': 'MultiImage Zoom For Product In WebSite',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'http://www.serpentcs.com',
    'version': '10.0.1.0.1',
    'license': 'AGPL-3',
    'depends': [
        'website_sale',
        'stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_images.xml',
        'views/templates.xml',
    ],
    'images': ['static/description/MultiImageZoom.png'],
    'installable': True,
}
