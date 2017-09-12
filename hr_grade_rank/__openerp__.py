# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2017 Serpent Consulting Services Pvt. Ltd.
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
    'name': 'HR-Grade Rank',
    'version': '9.0.0.1.0',
    'description': """
HR-Grade Rank
=============
This module is used to add grade of employees.
        """,
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'category': 'Human Resources',
    'website': 'https://www.serpentcs.com',
    'depends': ['hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_grade_rank_view.xml',
    ],
}
