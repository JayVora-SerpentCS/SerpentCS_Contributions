# See LICENSE file for full copyright and licensing details.

{
    # Module information
    "name": "Product Image for Sale",
    "version": "19.0.1.0.0",
    "category": "Sales Management",
    "sequence": "1",
    "summary": """Product Image for Quotation/Sale Reports.""",
    "description": """Product Image for Quotation/Sale Reports.""",
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
    "images": ["static/description/product_images_for_sale_product_banner.jpg"],
    # Techical
    "installable": True,
    "auto_install": False,
}
