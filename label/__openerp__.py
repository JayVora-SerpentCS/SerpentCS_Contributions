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
    "name" : "Mass Label Reporting",
    "version" : "1.0",
    "author" : "Serpent Consulting Services Pvt. Ltd.",
    "category" : "Tools",
    "website" : "http://www.serpentcs.com",
    "description": """
    The video : https://www.youtube.com/watch?v=Fps5FWfcLwo
    """,
    'depends': ['report_webkit'],
    'data': [
             'data/report_paperformat.xml',
             'security/label.brand.csv',
             'security/label.config.csv',
             'views/label_config_view.xml',
             'views/label_print_view.xml',
             'views/label_size_data.xml',
             'views/label_report.xml',
             'wizard/label_print_wizard_view.xml',
             'report/dynamic_label.xml'
    ],
    'installable': True,
    'auto_install': False,
}
