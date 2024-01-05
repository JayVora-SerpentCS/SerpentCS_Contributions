# See LICENSE file for full copyright and licensing details.

{
    "name": "Web Lead Funnel Chart",
    "category": "Web",
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "maintainer": "Serpent Consulting Services Pvt. Ltd.",
    "summary": "Funnel Chart for Leads & Opportunities",
    "website": "https://serpentcs.com",
    "version": "15s.0.1.0.0",
    'license': "LGPL-3",
    "depends": ["sale_crm"],
    "data": ["views/web_lead_funnel_chart_view.xml"],
    "images": ["static/description/FunnelChart.png"],
    'assets': {
        'web.assets_backend': [
            '/web_lead_funnel_chart/static/src/lib/highcharts.js',
            '/web_lead_funnel_chart/static/src/lib/funnel.js',
            '/web_lead_funnel_chart/static/src/js/web_lead_funnel_chart.js',
            '/web_lead_funnel_chart/static/src/xml/web_funnel_chart.xml',
        ],
    },
    "installable": True,
    "auto_install": False,
}
