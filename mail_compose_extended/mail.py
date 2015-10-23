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

from openerp.osv import fields, osv
from openerp import netsvc
from openerp import tools
from openerp.tools.translate import _
import re
import base64
import logging
from urllib import urlencode
from urlparse import urljoin
from openerp import SUPERUSER_ID
from openerp.osv.orm import except_orm

_logger = logging.getLogger(__name__)

class mail_mail(osv.Model):
    _inherit = ['mail.thread', 'mail.mail']
    _name = 'mail.mail'

    def _get_partner_access_link(self, cr, uid, mail, partner=None, context=None):
       """Generate URLs for links in mails: partner has access (is user):
       link to action_mail_redirect action that will redirect to doc or Inbox """
       if context is None:
           context = {}
       if partner:
           base_url = self.pool.get('ir.config_parameter').get_param(cr, uid, 'web.base.url')
           mail_model = mail.model or 'mail.thread'
           return "<span class='oe_mail_footer_access'><small>%(access_msg)s <a style='color:inherit' href='%(portal_link)s'>%(portal_msg)s</a></small></span>" % {
               'access_msg': _('about') if mail.record_name else _('access'),
               'portal_link': '',
               'portal_msg': '%s %s' % (context.get('model_name', ''), mail.record_name) if mail.record_name else _('your messages'),
           }
       else:
           return None

    def send_get_mail_body(self, cr, uid, mail, partner=None, context=None):
            """ Return a specific ir_email body. The main purpose of this method
                is to be inherited by Portal, to add a link for signing in, in
                each notification email a partner receives.
    
                :param browse_record mail: mail.mail browse_record
                :param browse_record partner: specific recipient partner
            """
            body = mail.body_html
            link = None
            if mail.notification or (mail.model and mail.res_id):
                link = self._get_partner_access_link(cr, uid, mail, partner, context=context)
            if link:
                body = tools.append_content_to_html(body, link, plaintext=False, container_tag='div')
            return body

    def send_get_mail_reply_to(self, cr, uid, mail, partner=None, context=None):
        """ Return a specific ir_email reply_to.
            :param browse_record mail: mail.mail browse_record
            :param browse_record partner: specific recipient partner
        """
        if mail.reply_to:
            return mail.reply_to
        email_reply_to = False

        # if model and res_id: try to use ``message_get_reply_to`` that returns the document alias
        if mail.model and mail.res_id and hasattr(self.pool.get(mail.model), 'message_get_reply_to'):
            email_reply_to = self.pool.get(mail.model).message_get_reply_to(cr, uid, [mail.res_id], context=context)[0]
        # no alias reply_to -> reply_to will be the email_from, only the email part
        if not email_reply_to and mail.email_from:
            emails = tools.email_split(mail.email_from)
            if emails:
                email_reply_to = emails[0]

        # format 'Document name <email_address>'
        if email_reply_to and mail.model and mail.res_id:
            user_name = self.pool.get("res.users").read(cr, uid, [uid], fields=["name"], context=context)[0]
            if user_name:
                email_reply_to = _("%s <%s>") % (user_name.get('name'), email_reply_to)
        return email_reply_to

    def send_get_email_dict(self, cr, uid, mail, partner=None, context=None):
        """ Return a dictionary for specific email values, depending on a
            partner, or generic to the whole recipients given by mail.email_to.

            :param browse_record mail: mail.mail browse_record
            :param browse_record partner: specific recipient partner
        """
        partner_obj = self.pool.get('res.partner')
        body = self.send_get_mail_body(cr, uid, mail, partner=partner, context=context)
        reply_to = self.send_get_mail_reply_to(cr, uid, mail, partner=partner, context=context)
        body_alternative = tools.html2plaintext(body)
        
        # generate email_to, heuristic:
        # 1. if 'partner' is specified and there is a related document: Followers of 'Doc' <email>
        # 2. if 'partner' is specified, but no related document: Partner Name <email>
        # 3; fallback on mail.email_to that we split to have an email addresses list
        
        new_email_to = []
        partner_obj = self.pool.get('res.partner')
        partner_ids = partner_obj.search(cr, uid, [('name', '=', mail.record_name)], context=context)
        
        if partner_ids:
            for partner in partner_ids:
                foll = partner_obj.browse(cr, uid, partner, context=context).message_follower_ids
                new_email_to.append(mail.email_to)
                if foll:
                    new_email_to.append(mail.email_to)
                    for partner_to_send in partner_obj.browse(cr, uid, partner, context=context).message_follower_ids:
                        if partner_to_send and mail.record_name:
                            sanitized_record_name = re.sub(r'[^\w+.]+', '-', mail.record_name)
                            email_to = _('%s <%s>') % (partner_to_send.name, partner_to_send.email)
                            new_email_to.append(email_to)
                        elif partner_to_send:
                            email_to = '%s <%s>' % (partner_to_send.name, partner_to_send.email)
                            new_email_to.append(email_to)
                else:
                    new_email_to.append(mail.email_to)
        else:
            
            for partner in mail.partner_ids:
                if partner and mail.record_name:
                    sanitized_record_name = re.sub(r'[^\w+.]+', '-', mail.record_name)
                    email_to = _('%s <%s>') % (partner.name, partner.email)
                    new_email_to.append(email_to)
                elif partner:
                    email_to = '%s <%s>' % (partner.name, partner.email)
                    new_email_to.append(email_to)
                else:
                    new_email_to = tools.email_split(mail.email_to)
        return {
            'body': body,
            'body_alternative': body_alternative,
            'subject': self.send_get_mail_subject(cr, uid, mail, partner=partner, context=context),
            'reply_to': reply_to,
            'email_to': new_email_to,
        }

    def send(self, cr, uid, ids, auto_commit=False, recipient_ids=None, context=None):
        """ Sends the selected emails immediately, ignoring their current
            state (mails that have already been sent should not be passed
            unless they should actually be re-sent).
            Emails successfully delivered are marked as 'sent', and those
            that fail to be deliver are marked as 'exception', and the
            corresponding error mail is output in the server logs.

            :param bool auto_commit: whether to force a commit of the mail status
                after sending each mail (meant only for scheduler processing);
                should never be True during normal transactions (default: False)
            :param list recipient_ids: specific list of res.partner recipients.
                If set, one email is sent to each partner. Its is possible to
                tune the sent email through ``send_get_mail_body`` and ``send_get_mail_subject``.
                If not specified, one email is sent to mail_mail.email_to.
            :return: True
        """
        context = dict(context or {})
        ir_mail_server = self.pool.get('ir.mail_server')
        mail_server_ids = ir_mail_server.search(cr, uid, [], context=context)
        ir_attachment = self.pool['ir.attachment']
        for mail in self.browse(cr, SUPERUSER_ID, ids, context=context):
            if mail.model:
                model_id = self.pool['ir.model'].search(cr, SUPERUSER_ID, [('model', '=', mail.model)], context=context)[0]
                model = self.pool['ir.model'].browse(cr, SUPERUSER_ID, model_id, context=context)
            else:
                model = None
            if model:
                context['model_name'] = model.name
            try:
                # handle attachments
                attachments = []
                for attach in mail.attachment_ids:
                    attachments.append((attach.datas_fname, base64.b64decode(attach.datas)))
                # specific behavior to customize the send email for notified partners

                email_list = []
                if mail.email_to:
                    email_list.append(self.send_get_email_dict(cr, uid, mail, mail.res_id, context=context))
                else:
                    email_list.append(self.send_get_email_dict(cr, uid, mail, context=context))
                # build an RFC2822 email.message.Message object and send it without queuing
                res = None
                
                for email in email_list:
                    msg = ir_mail_server.build_email(
                        email_from=mail.email_from,
                        email_to=email.get('email_to'),
                        subject=email.get('subject'),
                        body=email.get('body'),
                        body_alternative=email.get('body_alternative'),
                        email_cc=tools.email_split(mail.email_cc),
                        reply_to=email.get('reply_to'),
                        attachments=attachments,
                        subtype='html')
                    res = ir_mail_server.send_email(cr, uid, msg, mail_server_id=mail.mail_server_id.id, context=context)
                if res:
                    mail.write({'state': 'sent', 'message_id': res})
                    mail_sent = True
                else:
                    mail.write({'state': 'exception'})
                    mail_sent = False

                # /!\ can't use mail.state here, as mail.refresh() will cause an error
                # see revid:odo@openerp.com-20120622152536-42b2s28lvdv3odyr in 6.1
                if mail_sent:
                    self._postprocess_sent_message(cr, uid, mail, context=context)
            except MemoryError:
                # prevent catching transient MemoryErrors, bubble up to notify user or abort cron job
                # instead of marking the mail as failed
                raise
            except Exception:
                _logger.exception('failed sending mail.mail %s', mail.id)
                mail.write({'state': 'exception'})

            if auto_commit == True:
                cr.commit()
        return True

class mail_compose_message(osv.Model):
    _inherit = 'mail.compose.message'

    def generate_email_for_composer(self, cr, uid, template_id, res_id, context=None):
        """ Call email_template.generate_email(), get fields relevant for
            mail.compose.message, transform email_cc and email_to into partner_ids """
        values = super(mail_compose_message, self).generate_email_for_composer(cr, uid, template_id, res_id, context=context)
        if context.get('active_model'):
            Values = [x.id for x in self.pool.get(context.get('active_model')).browse(cr, uid, res_id).message_follower_ids]
            if 'partner_ids' not in values.keys():
                values['partner_ids'] = []
            values['partner_ids'] += Values
        return values


class mail_notification(osv.Model):
    """ Class holding notifications pushed to partners. Followers and partners
        added in 'contacts to notify' receive notifications. """
    _inherit = 'mail.notification'

    def _notify(self, cr, uid, msg_id, partners_to_notify=None, context=None):
        """ Send by email the notification depending on the user preferences
          321  :param list partners_to_notify: optional list of partner ids restricting
                the notifications to process
        """
        if context is None:
            context = {}

        if 'only_recipents' in context.keys():
            partners_to_notify = context['only_recipents']

        return super(mail_notification, self)._notify(cr, uid, msg_id, partners_to_notify, context)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

