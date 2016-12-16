# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Project Dates on Kanban',
    'version': '9.0.1.0.1',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'http://www.serpentcs.com',
    'summary': """Find Idle projects - Displays last updated date and recent updated
                date for the Project.""",
    'depends': ['project'],
    'category': 'Project Management',
    'sequence': 1,
    'data': [
        'views/project_kanban_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
