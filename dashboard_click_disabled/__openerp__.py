# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011-Today Serpent Consulting Services Pvt. Ltd. 
#    (<http://www.serpentcs.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

{
    # Module information
    'name': "Disable click Inside List view on Dashboard",
    'description': """
    """,
    'category': 'web',
    'version': '1.0',
    'depends': ['board'],
     "description": """
Disable the click on the List views of Dashbaord.
=================================

Usually the Dashboard contains various views combined,
which are the list, calendar and Graph views; clicking on which leads you
to the Form view of a record.

As a manager this might look annoying to you as your clear purpose is just to
view and analyse the business documents.

This module gives you the disability from that clickable behaviour. 
""",

    # Templates and Snippets
    'data': [
        'views/board.xml',
    ],

    # Author information
    'author': "Serpent Consulting Services Pvt. Ltd.",
    'website': "http://www.serpentcs.com",
    'installable': True,
}