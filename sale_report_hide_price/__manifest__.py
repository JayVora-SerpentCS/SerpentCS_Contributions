# -*- coding: utf-8 -*-
# © 2016 Serpent Consulting Services Pvt. Ltd. <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Hide Price and Discount in Quotation Report',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'category': 'Sales Management',
    'website': 'http://www.serpentcs.com',
    'version': '10.0.1.0.1',
    'license': 'AGPL-3',
    'summary': 'Hide price/discount in Sale Order Report',
    'description': '''This module is to hide price/discount in Sale Order
        Report.
        It would give you 2 additional fields on Sales Order / Quotation:
        1. Show Price
        2. Show Discount Based on the choices on the fields, the relevant
        fields would be shown on the report.''',
    'depends': ['sale'],
    'data': ['views/sale_view.xml',
             'views/report_saleorder.xml'
             ],
    'installable': True,
    'auto_install': False
}
