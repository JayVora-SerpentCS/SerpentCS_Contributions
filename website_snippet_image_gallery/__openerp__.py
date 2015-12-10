# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015-Serpentcs (<http://www.serpentcs.com>).
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
    'name': 'Website Snippet Image Gallery',
    'category': 'Theme',
    'summary': 'Adds image gallery in website',
    'version': '8.0.1.0.0',
    'description': """Image Gallery Snippet""",
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'depends': ['website', 'website_less'],
    'data': [
        'views/assets.xml',
        'views/image-gallery-snippet.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
