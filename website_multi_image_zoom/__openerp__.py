# -*- encoding: UTF-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-Today Serpent Consulting Services PVT. LTD.
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
    'name': 'Website Product Multi-Image Zoom',
    'category': 'Website',
    'summary': 'MultiImage Zoom For Product In WebSite',
    'author': 'Serpent Consulting Services Pvt. Ltd.,'
              'Odoo Community Association (OCA)',
    'website': 'http://www.serpentcs.com',
    'version': '9.0.1.0.1',
    'depends': [
        'website_sale',
        'stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_images.xml',
        'views/templates.xml',
    ],
    'installable': True,
}
