# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2011-2014 Serpent Consulting Services Pvt. Ltd.
#                                        (<http://serpentcs.com>).
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
    'name': 'Web one2many Kanban',
    'version': '1.0.1',
    'sequence': 6,
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'description' : """
        You need to define o2m field in kanban view definition and use
        for loop to display fields like:

        <t t-foreach="record.o2mfield.raw_value" t-as='o'>
            <t t-esc="o.name">
        </t>
    """,
    'installable': True,
    'application': True,
    'data':[
            'view/templates.xml',
            ],
    'depends': ['web'],
    'auto_install': False,
}
