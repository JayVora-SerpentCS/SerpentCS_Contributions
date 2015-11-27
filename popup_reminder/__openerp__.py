# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Pop-up Reminder 9.0',
    'version': '1.0',
    'category': 'Base',
    'summary': 'Popup Reminder',
    'description': """
Automatic Reminder System
=========================

This module will provide generalised feature to configure various reminders on different models.

You can configure reminders on any parameter and set for the current month, today, next month, and daily basis. 

This module will help you to get reminders for :

* Employee's passport expiring next month
* Visa expiring on next month
* List of tasks having deadlines today
* List of tasks to be start today
* List of leads and opportunities having action date today
    """,
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'website' : 'http://www.serpentcs.com',
    'depends': ['base','web'],
    'data': [
        'security/ir.model.access.csv',
        'popup_reminder_view.xml',
        'views/popup_views.xml'
    ],
    'qweb': ['static/src/xml/view.xml'],
    'auto_install': False,
    'installable': True,
    'application': True,
    'price': 200,
    'currency': 'EUR',

}
