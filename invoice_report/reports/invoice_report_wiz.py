# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2017-TODAY Serpent Consulting Services Pvt. Ltd.
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
from openerp.report import report_sxw
from openerp.osv import osv


class invoice_report_parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        super(invoice_report_parser, self).__init__(
            cr, uid, name, context=context)
        self.localcontext.update({
            'get_total': self.get_total,
            'get_invoices': self.get_invoices,
        })

    def get_total(self):
        return self.total

    def get_invoices(self, data):
        date_start = data['form']['date_start']
        date_stop = data['form']['date_stop']
        inv_type = data['form']['inv_type']
        is_open = data['form']['is_open']
        states = ['draft', 'cancel']
        if not is_open:
            states.append('open')
        domain = [('date_invoice', '>=', date_start),
                  ('date_invoice', '<=', date_stop),
                  ('state', 'not in', states)]
        if inv_type:
            domain.append(('type', '=', inv_type))
        total_amnt = 0.0
        inv_obj = self.pool.get("account.invoice")
        inv_ids = inv_obj.search(self.cr, self.uid, domain,
                                 order="partner_id")
        invoice_ids = inv_obj.browse(self.cr, self.uid, inv_ids)
        for inv in invoice_ids:
            if inv.type in ['out_invoice', 'in_refund']:
                total_amnt += sum([pay.credit for pay in inv.payment_ids])
            elif inv.type in ['in_invoice', 'out_refund']:
                total_amnt += sum([pay.debit for pay in inv.payment_ids])
        self.total = total_amnt
        return invoice_ids


class invoice_report_profile(osv.AbstractModel):
    _name = 'report.invoice_report.invoice_report_wiz_template'
    _inherit = 'report.abstract_report'
    _template = 'invoice_report.invoice_report_wiz_template'
    _wrapped_report_class = invoice_report_parser
