#    Copyright (C) 2017 Serpent Consulting Services Pvt. Ltd.


{
    'name': 'Project Task Report',
    'version': '12.0.1.0.0',
    'category': 'Project Management',
    'license': 'AGPL-3',
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
