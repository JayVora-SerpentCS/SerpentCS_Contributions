# See LICENSE file for full copyright and licensing details.

from datetime import datetime

from odoo import api, models, _
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def check_limit(self):
        self.ensure_one()
        partner = self.partner_id
        moveline_obj = self.env['account.move.line']
        movelines = moveline_obj.search(
            [('partner_id', '=', partner.id),
             ('account_id.user_type_id.name', 'in', ['Receivable', 'Payable']),
             ('full_reconcile_id', '=', False)]
        )
        debit, credit = 0.0, 0.0
        today_dt = datetime.strftime(datetime.now().date(), DF)
        for line in movelines:
            if datetime.strftime(line.date_maturity, DF) < today_dt:
                credit += line.debit
                debit += line.credit

        if (credit - debit + self.amount_total) > partner.credit_limit:
            if not partner.over_credit:
                msg = 'Can not confirm Sale Order,Total mature due Amount ' \
                      '%s as on %s !\nCheck Partner Accounts or Credit ' \
                      'Limits !' % (credit - debit, today_dt)
                raise UserError(_('Credit Over Limits !\n' + msg))
            partner.write({'credit_limit': credit - debit + self.amount_total})
        return True

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            order.check_limit()
        return res
