# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2011-Till Today Serpent Consulting Services PVT. LTD.
#    (<http://www.serpentcs.com>)
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


from openerp.osv import osv, fields

class mail_compose_message(osv.TransientModel):
    _inherit = 'mail.compose.message'

    _columns = {
        'fwd_message': fields.boolean('Forward Message'),
    }
    _defaults = {
        'fwd_message': False
    }
    def get_record_data(self, cr, uid, values, context=None):
        if context is None:
            context = {}
        result = super(mail_compose_message,
                       self).get_record_data(cr, uid, values=values,
                                             context=context)
        if context.get('default_subject'):
            result['subject'] = context.get('default_subject')
        return result
