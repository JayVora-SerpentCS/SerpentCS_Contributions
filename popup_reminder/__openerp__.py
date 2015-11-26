# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-Today Serpent Consulting Services Pvt. Ltd.
#                                      (<http://www.serpentcs.com>)
#    Copyright (C) 2004 OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

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
