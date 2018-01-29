# Copyright 2016 Serpent Consulting Services Pvt. Ltd
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Web One2many Kanban",
    "version": "11.0.1.0.0",
    "sequence": 6,
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "maintainer": "Serpent Consulting Services Pvt. Ltd.",
    "website": "http://www.serpentcs.com",
    "license": "AGPL-3",
    'summary': 'Display one2many widget as kanban',
    "description": """
        You need to define o2m field in kanban view definition and use
        for loop to display fields like:

        <t t-foreach="record.o2mfield.raw_value" t-as="o">
            <t t-esc="o.name"/>
            <t t-esc="o.m2o_field[1]"/>
        </t>
    """,
    "depends": [
        "web",
    ],
    "data": [
        "view/templates.xml",
    ],
    "images": ["static/description/o2mKanban.png"],
    "installable": True,
    "application": True,
}
