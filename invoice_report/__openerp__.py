# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2017-TODAY Serpent Consulting Services Pvt. Ltd.
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
    'name': 'Report of Invoices with Payment Details',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'category': 'Reports',
    'website': "http://www.serpentcs.com",
    'version': '8.0.1.0.0',
    'description': "This Module Adds a report for invoices alongwith its \
payment details.",
    'depends': ['account'],
    'data': [
             'wizard/invoice_report_wizard.xml',
             'reports/invoice_report_template.xml',
             'reports/report_register_view.xml',
    ],
    'installable': True,
    'auto_install': False
}
