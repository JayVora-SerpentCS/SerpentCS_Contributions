# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 OpenERP SA (<http://www.openerp.com>)
#    Copyright (C) 2011-2015 Serpent Consulting Services Pvt. Ltd.
#    (<http://www.serpentcs.com>).
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
    "name" : "Web Widget Multi Image V8",
    "version" : "1.0",
    "author" : "Serpent Consulting Services Pvt. Ltd.",
    "category": 'Image',
    'complexity': "easy",
    'depends': ['product'],
    "description": """
    """,
    'data': [
        'view/templates.xml',
        'view/product_view.xml',
        ],
    'website': 'http://www.serpentcs.com',
    'qweb': ['static/src/xml/image_multi.xml'],
    'installable': True,
    'auto_install': False,
}
