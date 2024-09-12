# See LICENSE file for full copyright and licensing details.

{
    "name": "Applicant Process",
    "version": "17.0.0.1.0",
    "category": "Human Resources",
    "sequence": 90,
    "license": "LGPL-3",
    "summary": "Applicant and Employee Subsections, Training",
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "website": "http://www.serpentcs.com",
    "maintainer": "Serpent Consulting Services Pvt. Ltd.",
    "depends": ["hr_recruitment"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/select_training_view.xml",
        "report/report_view.xml",
        "views/hr_recruitment_views.xml",
        "views/hr_recruitment_employee_views.xml",
        "views/training_views.xml",
        "views/applicant_profile_report_view.xml",
    ],
    # Odoo App Store Specific
    "images": ["static/description/Banner_hr_applicant.png"],
    "installable": True,
    "application": True,
}
