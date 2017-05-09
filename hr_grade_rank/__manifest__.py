# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{
    'name': 'HR-Grade Rank',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'description': """
        HR-Grade Rank
        =============
        This module is used to add grade of employees.""",
    'author': 'Serpent Consulting Services Pvt. Ltd.,'
              'Odoo Community Association (OCA)',
    'category': 'Human Resources',
    'website': 'https://www.serpentcs.com',
    'depends': ['hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_grade_rank_view.xml',
    ],
}
