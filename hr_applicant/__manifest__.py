# -*- coding: utf-8 -*-
##############################################################################
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 Serpent Consulting Services (<http://serpentcs.com>).
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
#############################################################################

{
    'name': 'Applicant Process',
    'version': '10.0.0.1.0',
    'category': 'Human Resources',
    'sequence': 90,
    'summary': 'Applicant and Employee Subsections, Training',
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "website": "http://www.serpentcs.com",
    'license': 'AGPL-3',
    "maintainer": "Serpent Consulting Services Pvt. Ltd.",
    'depends': ['hr_recruitment', 'document'],
    'data': ['wizard/select_training_view.xml',
             'views/hr_recruitment_views.xml',
             'views/hr_recruitment_employee_views.xml',
             'views/training_views.xml',
             'views/applicant_profile_report_view.xml',
             'report/report_view.xml'
             ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 5,
    'currency': 'EUR',
}
