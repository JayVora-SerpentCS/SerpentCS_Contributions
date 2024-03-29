# See LICENSE file for full copyright and licensing details.

{
    "name": "iPushp - Employee Business Directory",
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "category": "Human Resource",
    "website": "http://www.serpentcs.com",
    "summary": "iPushp",
    "version": "17.0.1.0.0",
    "license": "AGPL-3",
    "description": "iPushp - Employee Business Directory",
    "depends": ["hr", "website"],
    "data": [
        "security/ir.model.access.csv",
        "data/website_data.xml",
        "data/relation_data.xml",
        "views/ipushp_config_view.xml",
        "views/hr_employee_view.xml",
        "views/website_ipushp_template.xml",
        "views/ipushp_search.xml",
        "views/find_contacts.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "ipushp/static/src/js/custom.js",
            "ipushp/static/src/css/fix_bg_snippet.css",
            "ipushp/static/src/css/style.css",
        ]
    },
    "images": ["static/description/page_1.png"],
    "installable": True,
    "currency": "EUR",
    "price": 27
}
