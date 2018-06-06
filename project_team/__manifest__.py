# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Project - Set Team and members',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'summary': 'Project Team Management',
    'category': 'Project Management',
    'website': 'http://www.serpentcs.com',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': ['project', 'crm', 'web'],
    'data': [
        'views/template.xml',
        'views/project_team_view.xml',
    ],
    'images': ['static/description/ProjectTeam.png'],
    'installable': True,
    'auto_install': False,
    'price': 5,
    'currency': 'EUR',
}
