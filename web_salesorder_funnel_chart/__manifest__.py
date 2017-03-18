# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Web Sales Order Funnel Chart 10.0',
    'category': 'Web',
    'author': "Serpent Consulting Services Pvt. Ltd.",
    'summary': 'Funnel Chart for Sales Order',
    'website': 'http://www.serpentcs.com',
    'version': '10.0.1.0.0',
    'depends': [
        'sale'
    ],
    'data': [
        "views/templates.xml",
        "views/web_sale_order_funnel_chart_view.xml"
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
