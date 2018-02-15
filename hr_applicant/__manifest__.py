# See LICENSE file for full copyright and licensing details.

{
    'name': 'Applicant Process',
    'version': '11.0.0.1.0',
    'category': 'Human Resources',
    'sequence': 90,
    'license': "AGPL-3",
    'summary': 'Applicant and Employee Subsections, Training',
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "website": "http://www.serpentcs.com",
    "maintainer": "Serpent Consulting Services Pvt. Ltd.",
    'depends': ['hr_recruitment', 'document'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/select_training_view.xml',
        'views/hr_recruitment_views.xml',
        'views/hr_recruitment_employee_views.xml',
        'views/training_views.xml',
        'views/applicant_profile_report_view.xml',
        'report/report_view.xml'
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
