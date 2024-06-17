# See LICENSE file for full copyright and licensing details.

{
    # Module information
    'name': 'POS Security Dialog',
    'version': '14.0.1.0.0',
    'license': 'AGPL-3',
    'category': 'Web',
    'summary': 'This module provides the functionality for POS security on the type of button.',
    'description': """This module provides the functionality for POS security on the type of button.""",
    
    # Author
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'https://www.serpentcs.com',
    
    # Dependancies
    'depends': ['point_of_sale', 'web_security_dialog'],
    
    # Views
    'data': [
        'views/pos_config_view.xml',
        'views/templates.xml'
    ],
    
    
    # Odoo App Store Specific
    'images': ['static/description/Odoo-app-pos-security-dailog.png'],
    
    # Technical
    'installable': True,
    'application': True
}
