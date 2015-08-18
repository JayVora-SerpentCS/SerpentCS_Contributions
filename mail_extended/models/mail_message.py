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
from openerp import api
from datetime import datetime
from openerp import tools

class mail_message(osv.Model):

    _inherit = 'mail.message'

    def _get_date(self, cr, uid, date, context=None):
        new_date = ''
        if date:
            date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            month = date.strftime('%a, %b %d, %Y')
            time = date.strftime('%H:%M')
            am_pm = date.strftime('%p')
            new_date = month+" at "+time+" "+am_pm
        return new_date

    @api.cr_uid_context
    def forward_message(self, cr, uid, ids=None, attachment_ids=[], context=None):
        message = '<br/><br/><div style="border-left:1px solid blue;margin-left:5%;">----Forwarded Message--- <br/>'
        subject = ''
        vals = {}
        for rec in self.browse(cr, uid, ids, context=context):
            #Add Forwarding Details
            message += 'From: <b>%s</b> &#60;%s&#62;'%(tools.ustr(rec.author_id.name), tools.ustr(rec.author_id.email))
            sent_date = self._get_date(cr, uid, rec.date, context=context)
            message += '<br/>Date: %s'%(str(sent_date))
            #Add subject for forwarded message
            temp_subject = rec.subject
            if rec.subject:
                message += '<br/>Subject: Fwd:%s'%(tools.ustr(rec.subject))
            if not rec.subject:
                temp_subject = rec.parent_id and rec.parent_id.subject or ''
            subject = "Fwd:"+tools.ustr(temp_subject)
            #Get details to which partner mail is sent
            to_details = ''
            count = 1
            max = len(rec.partner_ids)
            for partner in rec.partner_ids:
                if count == max:
                    to_details += '%s &#60;%s&#62;'%(tools.ustr(partner.name), tools.ustr(partner.email))
                else:
                    to_details += '%s &#60;%s&#62;,'%(tools.ustr(partner.name), tools.ustr(partner.email))
                count += 1
            message += '<br/>To: %s'%(str(to_details))
            #Add Body part
            message += '<br/>'
            message += '<br/>'
            child_message_ids = self.search(cr, uid, [('id', 'child_of',rec.id)], context=context)
            for msg in self.browse(cr, uid, child_message_ids, context=context):
                message += "On %s, %s wrote:"%(self._get_date(cr, uid, msg.date, context=context), msg.author_id.name)
                message += tools.ustr(msg.body)
        message += '</div>'
        vals.update({
             'default_body' : message, 
             'default_subject' : tools.ustr(subject),
             'default_fwd_message' : True,
        })
        if attachment_ids:
            vals.update({'default_attachment_ids' : [(6, 0, attachment_ids)]})
        return dict(vals)
