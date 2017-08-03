# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Web GroupBy Expand",
    "version": "10.0.1.0.0",
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "maintainer": "Serpent Consulting Services Pvt. Ltd.",
    "website": "http://www.serpentcs.com",
    "category": "Web",
    "license": "AGPL-3",
    'summary': 'Expand all groups on single click',
    "description": "Adds Expand button to expand all groups on a list view.",
    "depends": [
        "web",
    ],
    "data": [
        "views/templates.xml",
    ],
    "qweb": [
        "static/src/xml/web_groups_expand.xml",
    ],
    "images": ["static/description/groupexpand.png"],
    "installable": True,
}
