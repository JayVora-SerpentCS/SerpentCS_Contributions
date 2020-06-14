# See LICENSE file for full copyright and licensing details.

{
    "name": "Multi-DB Synchronization",
    "version": "12.0.1.0.0",
    "category": "Tools",
    "license": "AGPL-3",
    "summary": "Multi-DB Synchronization",
    "author": "OpenERP SA, Serpent Consulting Services Pvt. Ltd.",
    "website": "http://www.serpentcs.com",
    "maintainer": "Serpent Consulting Services Pvt. Ltd.",
    "images": [
        "static/description/Synchro.png",
    ],
    "depends": [
        "base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/base_synchro_view.xml",
        "views/base_synchro_view.xml",
        "views/res_request_view.xml",
    ],
    "installable": True,
}
