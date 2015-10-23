# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
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
    "name" : "Mass Label Reporting",
    "version" : "1.0",
    "author" : "Serpent Consulting Services Pvt. Ltd.",
    "category" : "Tools",
    "website" : "http://www.serpentcs.com",
    "description": """
    """,
    'depends': ['report_webkit'],
    'data': [
             'data/report_paperformat.xml',
             'security/label.brand.csv',
             'security/label.config.csv',
             'label_config_view.xml',
             'label_print_view.xml',
             'label_size_data.xml',
             'wizard/label_print_wizard_view.xml',
             'label_report.xml',
             'report/dynamic_label.xml'
    ],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
