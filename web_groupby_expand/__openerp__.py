# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011-Till Today Serpent Consulting Services PVT. LTD.
#                                          (<http://www.serpentcs.com>).
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
    "category": "Web",
    "version" : '7.0.1.0.0',
    "author" : 'Serpent Consulting Services Pvt. Ltd.',
    "description":
        """
A group by list can be expanded and collapased with buttons
===============================================================
You'll see two buttons appear on top right corner of the list when you perform a group by with which you can expand and collapse grouped records by level.
        """,
    "depends" : ["web"],
    "js": ["static/src/js/web_group_expand.js"],
    "css" : ["static/src/lib/font-awesome-4.5.0/css/font-awesome.css",
             "static/src/css/expand_buttons.css"],
    "qweb" : ["static/src/xml/expand_buttons.xml"],
    "installable": True,
    "auto_install": False,
}

