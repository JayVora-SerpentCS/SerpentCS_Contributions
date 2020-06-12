# See LICENSE file for full copyright and licensing details.

{
    'name': 'Project Report',
    'version': '12.0.1.0.0',
    'category': 'Project Management',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'license': 'LGPL-3',
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
