# Copyright 2016 Serpent Consulting Services Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Project - Status by Recent Activities',
    'version': '12.0.1.0.0',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'license': 'AGPL-3',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'http://www.serpentcs.com',
    'category': 'Project Management',
    'summary': """Find your Idle projects - Displays last
                updated date and recent updated date
                for the Project.""",
    'depends': [
        'project',
    ],
    'data': [
        'views/project_kanban_view.xml',
    ],
    'images': [
        'static/description/ProjectKanban.png',
    ],
    'installable': True,
}
