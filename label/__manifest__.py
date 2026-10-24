# See LICENSE file for full copyright and licensing details.
{
    "name": "Mass Label Reporting | Product Label Printing | Barcode Labels",
    "version": "20.0.1.0.0",
    "category": "Extra Tools",
    "license": "LGPL-3",
    "summary": (
        "Generate customised labels for any document | Product labels | "
        "Barcode labels | Bulk label printing"
    ),
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "website": "http://www.serpentcs.com",
    "maintainer": "Serpent Consulting Services Pvt. Ltd.",
    "depends": ["base", "web"],
    "data": [
        "data/report_paperformat.xml",
        "security/label.brand.csv",
        "security/label.config.csv",
        "security/ir.access.csv",
        "data/label_size_data.xml",
        "views/label_config_view.xml",
        "views/label_print_view.xml",
        "wizard/label_print_wizard_view.xml",
        "views/label_report.xml",
        "report/dynamic_label.xml",
    ],
    "uninstall_hook": "uninstall_hook",
    "images": ["static/description/mass_label_reporting_product_banner.gif"],
    "installable": True,
}
