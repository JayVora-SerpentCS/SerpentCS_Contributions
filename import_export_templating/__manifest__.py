# See LICENSE file for full copyright and licensing details.

{
    "name": "Import / Export Templating",
    "version": "16.0.1.0.0",
    "license": "LGPL-3",
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "maintainer": "Serpent Consulting Services Pvt. Ltd.",
    "website": "http://www.serpentcs.com",
    "category": "Base",
    "summary": """
    Standard import export template,
    User-friendly templates to upload download bulk data Manage easy
    import-export for non-technical users of ERP.
    """,
    "depends": ["web"],
    "data": [
    		"security/ir.model.access.csv",
    		"wizard/wiz_download_template_view.xml"
    	    ],
    # Odoo App Store Specific
    "images": ["static/description/Banner-Import  Export Templating-16.png"],
    "installable": True,
    "price": 30.0,
    "currency": "EUR",
    "assets": {
        "web.assets_backend": [
            "/import_export_templating/static/src/js/wizard_action.js",
        ],
    },
}
