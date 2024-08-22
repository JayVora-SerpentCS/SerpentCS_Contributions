# See LICENSE file for full copyright and licensing details.

{
    'name': 'Web Digital Signature',
    'version': '17.0.1.0.0',
    "category": "Tools",
    "summary": """
        Touch screen enable so user can add signature with touch devices.
        Digital signature can be very usefull for documents.
    """,
     "description": """
     This module provides the functionality to store digital signature
     Example can be seen into the User's form view where we have
        added a test field under signature.
    """,
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "website": "http://www.serpentcs.com/",
    'license': 'LGPL-3',
    'depends': ['web'],
    "images": ["static/description/Digital_Signature.jpg"],
    "data": ["views/users_view.xml"],
    "assets": {
        "web.assets_backend": [
            "/web_digital_sign/static/src/js/digital_sign.js",
            "/web_digital_sign/static/src/xml/digital_sign.xml",
        ],
    },
    'installable': True,
    'application': True,
}
