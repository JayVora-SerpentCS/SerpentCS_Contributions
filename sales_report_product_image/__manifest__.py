# See LICENSE file for full copyright and licensing details.

{
    # Module information
    "name": "Product Image for Sale | Sales Product Image | Sales Report Product Image",
    "version": "20.0.1.0.0",
    "category": "Sales",
    "sequence": "1",
    "summary": (
        "Product Image for Quotation/Sale Reports | Product Image in Sale Order | "
        "Quotation Report Product Image | Sale Order PDF Product Image | "
        "Print Product Image in Report | Product Image in Order Lines | "
        "Big Medium Small Image Size"
    ),
    "description": (
        "Product Image for Sale | Sales Product Image | Sales Report Product Image"
    ),
    "license": "LGPL-3",
    # Author
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "website": "http://www.serpentcs.com",
    "maintainer": "Serpent Consulting Services Pvt. Ltd.",
    # Dependencies
    "depends": ["sale_management"],
    # Views
    "data": ["views/sale_product_view.xml", "views/report_saleorder.xml"],
    # Odoo App Store Specific
    "images": ["static/description/product_images_for_sale_product_banner.gif"],
    # Techical
    "installable": True,
    "auto_install": False,
}
