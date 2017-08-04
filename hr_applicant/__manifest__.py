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
    'description': """
Extend features of recruitment process and Manage Training
==========================================================

This application allows you to keep description for details of Applicant and Employee like Education, Language, Previous Occupation, 
Previous Travel, Medical Details and Relatives in form of Subsections.

Also allows you to manage training after employment if needed.
""",
    "author" : "Serpent Consulting Services Pvt. Ltd.",
    "website" : "http://www.serpentcs.com",
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
}
