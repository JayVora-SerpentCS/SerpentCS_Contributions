# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Web GroupBy Expand",
    "version": "9.0.1.0.0",
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "website": "http://www.serpentcs.com",
    "category": "Web",
    "description": "Adds Expand button to expand all groups on a list view.",
    "license": "AGPL-3",
    'summary': 'Expand all groups on single click',
    "depends": [
        "web",
    ],
    "data": [
        "views/templates.xml",
    ],
    "images": ["static/description/web-group-expand-banner.png"],
    "qweb": [
        "static/src/xml/web_groups_expand.xml",
    ],
    "installable": True,
}
