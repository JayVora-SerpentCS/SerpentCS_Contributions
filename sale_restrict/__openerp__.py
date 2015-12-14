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
    'name': "SO - Product Price Check",
    'summary': "SO - Product Price Check and restrict a user from confirming sale if product's sale price is zero.",
    'description': """
        This module restricts a user from confirming a Sale Order/Quotation if it contains products having sale price zero.
    """,
    'author': "Serpent Consulting Services Pvt. Ltd.",
    'website': "http://www.serpentcs.com",
    'category': 'Sales Management',
    'version': '8.0.0.1',
    'depends': ['sale'],
    'installable':True,
    'auto_install':False
}
