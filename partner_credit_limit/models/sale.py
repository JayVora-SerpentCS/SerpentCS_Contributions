# See LICENSE file for full copyright and licensing details.
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def check_limit(self, additional_amount=0.0):
        self.ensure_one()
        # Credit limits and outstanding receivables use the company currency.
        current_amount = self.amount_total / self.currency_rate + additional_amount
        self.partner_id.commercial_partner_id.with_company(
            self.company_id
        )._check_credit_limit_for_amount(
            self,
            current_amount=current_amount,
        )
        return True

    def action_confirm(self):
        pending_amounts = {}
        for order in self:
            key = (order.company_id.id, order.partner_id.commercial_partner_id.id)
            pending_amount = pending_amounts.get(key, 0.0)
            order.check_limit(additional_amount=pending_amount)
            # All checks run before super confirms the batch, so reserve the
            # earlier quotations' amounts when checking the next quotation.
            pending_amounts[key] = (
                pending_amount + order.amount_total / order.currency_rate
            )
        return super().action_confirm()
