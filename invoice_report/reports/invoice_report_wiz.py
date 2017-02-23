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
        super(invoice_report_parser, self).__init__(cr, uid, name,
                                                    context=context)
        self.localcontext.update({
            'get_invoice': self.get_invoice,
            'get_credit': self.get_credit,
            })

    def get_invoice(self, date_start, date_stop):
        result = {}
        sum = 0.0
        inv_obj = self.pool.get("account.invoice")
        inv_ids = inv_obj.search(self.cr, self.uid,
                                 [('date_invoice', '>=', date_start),
                                  ('date_invoice', '<=', date_stop),
                                  ('type', '=', 'out_invoice'),
                                  ('state', 'not in', ['draft', 'cancel'])],
                                 order="partner_id")
        invoice_ids = inv_obj.browse(self.cr, self.uid, inv_ids)

        for inv in invoice_ids:
            for pay in inv.payment_ids:
                sum += pay.credit
        user = self.pool.get("res.users").browse(self.cr, self.uid, self.uid)
        cur = user and user.company_id and user.company_id.currency_id
        return {'inv_ids': invoice_ids,
                'total': cur.name + cur.symbol + str("{0:,.2f}".format(sum))}

    def get_credit(self, pay, inv):
        result = {
                'currency_name': inv.currency_id.name,
                'currency_symbol': inv.currency_id.symbol,
                'credit': "{0:,.2f}".format(pay.credit),
                }
        return result


class invoice_report_profile(osv.AbstractModel):
    _name = 'report.invoice_report.invoice_report_wiz_template'
    _inherit = 'report.abstract_report'
    _template = 'invoice_report.invoice_report_wiz_template'
    _wrapped_report_class = invoice_report_parser
