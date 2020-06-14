#    Copyright (C) 2017 Serpent Consulting Services Pvt. Ltd.
#    Copyright (C) 2017 OpenERP SA (<http://www.serpentcs.com>)
#    License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


{
    'name': 'Project Task Report',
    'version': '12.0.1.0.0',
    'category': 'Project Management',
    'license': 'LGPL-3',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'http://www.serpentcs.com',
    'summary': """
      Print task details with all worklog entries and task hours summary""",
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'depends': [
        'hr_timesheet',
    ],
    'data': [
        'views/project_task_report.xml',
        'report/project_task_qweb_report.xml'
    ],
    'installable': True,
}
