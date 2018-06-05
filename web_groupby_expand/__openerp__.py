# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011-Till Today Serpent Consulting Services PVT. LTD.
#    (<http://www.serpentcs.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name": "Web GroupBy Expand",
    "version": "8.0.0.0.1",
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "website": "http://www.serpentcs.com",
    'category': 'Web',
    "license": "AGPL-3",
    "images": ["static/description/web-group-expand-banner.png"],
    "description": "Adds Expand button to expand all groups on a list view.",
    'summary': 'Expand all groups on single click',
    "depends": ["web"],
    'data': [
        'views/templates.xml',
    ],
    "qweb": ["static/src/xml/web_groups_expand.xml"],
    'installable': True,
    "auto_install": False,
}
