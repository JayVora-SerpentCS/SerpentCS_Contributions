# See LICENSE file for full copyright and licensing details.

{
    'name': 'Web Lead Funnel Chart',
    'category': 'Web',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'summary': 'Funnel Chart for Leads & Opportunities',
    'website': 'http://www.serpentcs.com',
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'crm',
        'sale',
    ],
    'data': [
        "views/templates.xml",
        "views/web_lead_funnel_chart_view.xml"
    ],
    'images': ['static/description/FunnelChart.png'],
    'installable': True,
    'auto_install': False,
}
