# See LICENSE file for full copyright and licensing details.

{
    'name': 'HR-Grade Rank',
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'summary': 'Manage grade and rank of employee',
#    'description': """
#        HR-Grade Rank
#        =============
#        This module is used to add grade of employees.""",
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'category': 'Human Resources',
    'website': 'https://www.serpentcs.com',
    'depends': ['hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_grade_rank_view.xml',
    ],
    'images': ['static/description/HRGradeRank.png'],
    'licence': 'AGPL-3',
    'sequence': 1,
    'installable': True,
    'auto_install': False,
}
