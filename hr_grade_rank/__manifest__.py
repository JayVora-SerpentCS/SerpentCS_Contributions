# See LICENSE file for full copyright and licensing details.

{
    'name': 'HR-Grade Rank',
    'version': '12.0.1.0.0',
    'license': 'LGPL-3',
    'summary': 'Manage grade and rank of employee',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'category': 'Human Resources',
    'website': 'http://www.serpentcs.com',
    'depends': ['hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_grade_rank_view.xml',
    ],
    'images': ['static/description/HRGradeRank.png'],
    'licence': 'LGPL-3',
    'sequence': 1,
    'installable': True,
    'auto_install': False,
}
