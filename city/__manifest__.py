# See LICENSE file for full copyright and licensing details.

{
    # Module Information
    "name": "City-Helps to keep Homogeneous address data in the Database",
    "version": "13.0.1.0.0",
    "category": "Hidden",
    "license": "AGPL-3",
    "summary": "City-Helps to keep Homogeneous address data in the Database",

    # Author
    "author": "Pablo Rocandio, Serpent Consulting Services Pvt. Ltd.",
    "website": "http://www.serpentcs.com",
    "maintainer": "Serpent Consulting Services Pvt. Ltd.",

    # Dependencies
    "depends": ["sales_team", "crm"],

    # Data
    "data": [
        "views/city_view.xml",
        "security/ir.model.access.csv",
    ],

    # Technical
    "installable": True,
    "auto_install": False,
}
