# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-Till Today Serpent Consulting Services PVT LTD 
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
############################################################################

{
    'name': 'Partner Follows List',
    'version': '1.0',
    'category': 'Partner',
    'description': """
    This module will give you the possibility to see what User/Partner
    follows what documents and records of those business documents.
    
    """,
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'website': ' http://www.serpentcs.com',
    'depends': ['mail'],
    'data': [
        'views/mail_followers.xml',
        'views/res_partner_view.xml',
             ],
    'installable': True,
    'active': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
