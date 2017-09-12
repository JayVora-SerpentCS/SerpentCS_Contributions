# -*- coding: utf-8 -*-
# Author: Guewen Baconnier
# Copyright 2013 Camptocamp SA
# Copyright 2016 Serpent Consulting Services Pvt. Ltd.
# (http://www.serpentcs.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Cancel Reason',
    'version': '10.0.1.0.0',
    'author': 'Camptocamp, Odoo Community Association (OCA)',
    'category': 'Sale',
    'license': 'AGPL-3',
    'complexity': 'normal',
    'website': 'http://www.camptocamp.com',
    'summary': 'Add sale cancellation reason',
    'description': """
        Sale Cancel Reason
        ==================
        When a sale order is canceled, a reason must be given,
        it is chosen from a configured list. """,
    'depends': ['sale'],
    'data': [
            'wizard/cancel_reason_view.xml',
            'view/sale_view.xml',
            'security/ir.model.access.csv',
            'data/sale_order_cancel_reason.xml',
        ],
    'images': ['static/description/SaleCancelReason.png'],
    'auto_install': False,
    'installable': True,
}
