# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Web one2many Kanban',
    'version': '1.0',
    'sequence': 6,
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'description': """
        You need to define o2m field in kanban view definition and use
        for loop to display fields like:

        <t t-foreach="record.o2mfield.raw_value" t-as='o'>
            <t t-esc="o.name">
        </t>
    """,
    'installable': True,
    'application': True,
    'data': [
        'view/templates.xml',
    ],
    'depends': ['web'],
    'auto_install': False,
}
