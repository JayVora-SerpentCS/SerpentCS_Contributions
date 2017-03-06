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
from datetime import datetime, date
from openerp import models, fields, api
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT


class invoice_report_wiz(models.TransientModel):
    _name = "inv.rpt.wiz"

    date_start = fields.Date('Start Date')
    date_stop = fields.Date('End Date')
    inv_type = fields.Selection([('out_invoice', 'Customer Invoice'),
                                 ('in_invoice', 'Supplier Invoice'),
                                 ('out_refund', 'Customer Refund'),
                                 ('in_refund', 'Supplier Refund'),
                                 ], 'Type', default="out_invoice")
    is_open = fields.Boolean('Open Invoice')

    @api.multi
    def _check_dates(self):
        start = self.date_start or False
        end = self.date_stop or False
        if start and end:
            if start > end:
                return False
        return True

    _constraints = [
        (_check_dates, 'Error! start-date must be lower than end-date.',
            ['date_start', 'date_stop'])
    ]

    @api.model
    def default_get(self, fields):
        cur_date = datetime.today().date()
        st_date = date(cur_date.year, cur_date.month, 1)
        stop_dt = datetime.strftime(cur_date,
                                    DEFAULT_SERVER_DATE_FORMAT)
        start_dt = datetime.strftime(st_date,
                                     DEFAULT_SERVER_DATE_FORMAT)
        res = super(invoice_report_wiz, self).default_get(fields)
        res.update({'date_start': start_dt,
                    'date_stop': stop_dt})
        return res

    @api.multi
    def print_report(self):
        if self._context is None:
            self._context = {}

        data = {
            'ids': self.ids,
            'model': 'account.invoice',
            'form': self.read()[0]
        }
        template = 'invoice_report.invoice_report_wiz_template'
        return self.env['report'].get_action(self, template, data=data)
