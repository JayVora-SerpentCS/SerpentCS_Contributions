# See LICENSE file for full copyright and licensing details.

{
    'name': 'iPushp',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'category': 'Human Resource',
    'website': "http://www.serpentcs.com",
    'summary':'iPushp',
    'version': '12.0.1.0.0',
    'description': "",
    'depends': ['hr', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'data/website_data.xml',
        'data/relation_data.xml',
        'views/assets.xml',
        'views/ipushp_config_view.xml',
        'views/hr_employee_view.xml',
        'views/website_ipushp_template.xml',
        'views/ipushp_search.xml',
        'views/find_contacts.xml',
    ],
    'installable': True,
    'auto_install': False
}
