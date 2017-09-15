# -*- coding: utf-8 -*-
# © 2016 Serpent Consulting Services Pvt. Ltd. <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Hide Price and Discount in Quotation Report',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'category': 'Sales Management',
    'website': 'http://www.serpentcs.com',
    'version': '9.0.1.0.1',
    'license': 'AGPL-3',
    'summary': 'Hide price/discount in Sale Order Report',
    'depends': ['sale'],
    'data': ['views/sale_view.xml',
             'views/report_saleorder.xml'
             ],
    'installable': True,
    'auto_install': False
}
