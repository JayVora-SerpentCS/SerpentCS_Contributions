# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Web GroupBy Expand",
    "version": "1.0",
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "website": "http://www.serpentcs.com",
    'category' : 'Web',
    "description": "Adds Expand button to expand all groups on a list view.",
    "depends": ["web"],
    'demo' : [],
    'data': [
        'views/templates.xml',
    ],
    "qweb": [ "static/src/xml/web_groupby_expand.xml" ],
    "auto_install": False,
}
