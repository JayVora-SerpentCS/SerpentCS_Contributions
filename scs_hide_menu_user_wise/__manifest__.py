# See LICENSE file for full copyright and licensing details.
{
    "name": "User-Based Menu Hiding",
    "version": "18.0.1.0.0",
    "category": "Additional Tools",
    "summary": "Hide Menus Based on User Roles, Odoo18 Menu Restriction, User-Specific Menu Customization, Odoo Apps",
    "description": "Allows hiding specific menu items based on user roles, providing custom menu visibility.",
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "company": "Serpent Consulting Services Pvt. Ltd.",
    "maintainer": "Serpent Consulting Services Pvt. Ltd.",
    "website": "https://www.serpentcs.com",
    "depends": ["base"],
    "data": [
        "security/security.xml",
        "views/res_users_views.xml",
    ],
    # Odoo App Store Specific
    "images": ["static/description/banner_hide_menu_user_wise.jpg"],
    "license": "LGPL-3",
    "installable": True,
    "auto_install": False,
    "application": False,
}
