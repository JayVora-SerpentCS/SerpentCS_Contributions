# Copyright 2016 Serpent Consulting Services Pvt. Ltd
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Web One2many Kanban",
    "version": "13.0.1.0.1",
    "license": "AGPL-3",
    "sequence": 6,
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "maintainer": "Serpent Consulting Services Pvt. Ltd.",
    "website": "http://www.serpentcs.com",
    "summary": "Display one2many widget as kanban",
    "description": """
        You need to define one2many field in kanban view definition and use
        for loop to display fields like:
        <t t-foreach="record.one2manyfield.raw_value" t-as='o'>
            <t t-esc="o.name">
            <t t-esc="o.many2onefield[1]">
        </t>""",
    "depends": ["web"],
    "data": ["view/templates.xml"],
    "images": ["static/description/o2mKanban.png"],
    "installable": True,
    "application": True,
}
