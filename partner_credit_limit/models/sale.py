# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
import logging
from odoo import api, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = "sale.order"

    def check_limit(self):
        self.ensure_one()
        if self.partner_id.commercial_partner_id:
            partner = self.partner_id.commercial_partner_id
        else:
            partner = self.partner_id
        move_lines = self.env['account.move.line'].search(
            [('partner_id', '=', partner.id),
             ('account_id.user_type_id.id', 'in', [
                 self.env.ref('account.data_account_type_receivable').id,
                 self.env.ref('account.data_account_type_payable').id]),
             ('full_reconcile_id', '=', False),
             ('company_id', '=', self.env.user.company_id.id)]
        )

        debit, credit = 0.0, 0.0
        for line in move_lines:
            credit += line.debit
            debit += line.credit

        if self.currency_id == self.env.user.company_id.currency_id:
            amount_total = self.amount_total
        else:
            amount_total = self.amount_total / self.currency_id.rate
        _logger.info(
            'move_lines: %s, debit: %s, credit: %s, amount_total: %s' % (move_lines, debit, credit, amount_total))
        if (credit - debit + amount_total) > partner.credit_limit:
            if not partner.over_credit:
                msg = 'Can not confirm Sale Order, Total mature due Amount ' \
                      '%s.\nCheck Partner Accounts or Credit ' \
                      'Limits !' % (credit - debit)
                raise UserError(_('Credit Over Limits:\n' + msg))
            partner.write(
                {'credit_limit': credit - debit + amount_total, 'over_credit': False, })
        return True

    @api.multi
    def action_confirm(self):
        for record in self:
            record.check_limit()
        res = super(SaleOrder, self).action_confirm()
        return res
