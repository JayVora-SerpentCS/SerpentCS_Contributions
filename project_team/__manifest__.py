# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Project - Set Team and members',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'summary': 'Adds Project Team Members.',
    'category': 'Project Management',
    'website': 'http://www.serpentcs.com',
    'version': '10.0.1.0.0',
    'sequence': 1,
    'depends': ['project', 'crm', 'web'],
    'data': [
        'views/template.xml',
        'views/project_team_view.xml',
    ],
    'installable': True,
    'auto_install': False
}
