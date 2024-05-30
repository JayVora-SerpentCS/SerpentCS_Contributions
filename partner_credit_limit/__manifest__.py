# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Partner Credit Limit',
    'version': '11.0.1.0.0',
    'category': 'Partner',
    'license': 'AGPL-3',
    'author': 'Tiny, Serpent Consulting Services Pvt. Ltd.',
    'website': 'http://www.serpentcs.com',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'summary': 'Set credit limit warning',
    'description': '''Partner Credit Limit'
        Checks for all over due payment and already paid amount
        if the difference is positive and acceptable then Salesman
        able to confirm SO
    ''',
    'depends': [
        'sale',
    ],
    'data': [
        'views/partner_view.xml',
    ],
    'installable': True,
}
