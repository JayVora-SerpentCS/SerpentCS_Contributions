# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{
    "name": "Multi-DB Synchronization",
    "version": "10.0.1.0.0",
    "category": "Tools",
    "description": """
Synchronization with all objects.
=================================

Configure servers and trigger synchronization with its database objects.
This module will let you synchronize two Odoo Databases!
""",
    "author": "OpenERP SA, Serpent Consulting Services Pvt. Ltd.",
    "images": ['images/1_servers_synchro.jpeg',
               'images/2_synchronize.jpeg',
               'images/3_objects_synchro.jpeg'],
    "depends": ["base"],
    'website': "http://www.serpentcs.com",
    "data": [
        "security/ir.model.access.csv",
        "wizard/base_synchro_view.xml",
        "views/base_synchro_view.xml",
        "views/res_request_view.xml",
    ],
    "installable": True,
    "auto_install": False,
}
