# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Web Lead Funnel Chart 10.0',
    'category': 'Web',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'summary': 'Funnel Chart for Leads & Opportunities',
    'website': 'http://www.serpentcs.com',
    'version': '10.0.2.0.0',
    'license': 'AGPL-3',
    'depends': [
        'crm'
    ],
    'data': [
        "data/crm_stage_data.xml",
        "views/templates.xml",
        "views/web_lead_funnel_chart_view.xml"
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'images': ['static/description/funnel.jpg'],
    'installable': True,
    'auto_install': False,
}
