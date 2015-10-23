# -*- coding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011-Today Serpent Consulting Services Pvt Ltd (<http://www.serpentcs.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################

{
    'name' : 'Mail Compose Extended',
    'version': '1.0',
    'author' : 'Serpent Consulting Services Pvt. Ltd.',
    'website' : 'http://www.serpentcs.com',
    'category': 'Email',
    'depends' : ['mail', 'account'],
    'description': """
   When an OpenERP login user (res.users) add a new email address during the
process of sending a email related to an object, this new email address will not be added to
the follower list of the related object.
  - TO and CC are seen when the emails are received.
  - Dynamically emails can be chosen while sending emails.

    """,
    'data': [
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
