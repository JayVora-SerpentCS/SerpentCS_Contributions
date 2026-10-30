# See LICENSE file for full copyright and licensing details.

{
    "name": "Partner Credit Limit | Odoo Customer Credit Limit | Odoo Credit Limit Warning",
    "version": "20.0.1.0.0",
    "summary": """
    Partner Credit Limit | Odoo Customer Credit Limit | Odoo Credit Limit Warning |
    Odoo Sales Order Credit Limit | Odoo Credit Limit Control | Odoo Partner Credit Management |
    Odoo Customer Credit Management | Odoo Credit Limit Alert | Odoo Credit Limit Restriction |
    Odoo Customer Credit Control | Odoo Credit Risk Management | Odoo Credit Limit Module
    """,
    "category": "Partner",
    "sequence": 1,
    "license": "AGPL-3",
    "author": "Tiny, Serpent Consulting Services Pvt. Ltd.",
    "website": "https://www.serpentcs.com",
    "maintainer": "Serpent Consulting Services Pvt. Ltd.",
    "depends": [
        "account",
        "sale_management",
    ],
    "data": [
        "views/partner_view.xml",
    ],
    "images": ["static/description/partner_credit_limit_product_banner.gif"],
    "installable": True,
}
