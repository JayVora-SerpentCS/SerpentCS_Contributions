# -*- coding: utf-8 -*-
# Copyright 2016 Serpent Consulting Services Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Project - Status by Recent Activities',
    'version': '10.0.1.0.0',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'http://www.serpentcs.com',
    'summary': """Find your Idle projects - Displays last
                updated date and recent updated date
                for the Project.""",
    'depends': ['project'],
    'category': 'Project Management',
    'license': 'AGPL-3',
    'sequence': 1,
    'data': ['views/project_kanban_view.xml'],
    'images': ['static/description/ProjectKanban.png'],
    'installable': True,
    'auto_install': False,
    'price': 5,
    'currency': 'EUR',
}
