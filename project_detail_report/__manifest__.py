# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Project Report',
    'version': '11.0.1.0.0',
    'category': 'Project Management',
    'description': """
      This module used to print report of project details.""",
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'http://www.serpentcs.com',
    'summary': """
      Print Project Detail report with task list and task details.""",
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'depends': [
        'hr_timesheet',
    ],
    'data': [
        'views/project_report.xml',
        'report/project_qweb_report.xml',
    ],
    'installable': True,
}
