# See LICENSE file for full copyright and licensing details.
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def check_limit(self):
        self.ensure_one()
        self.with_company(self.company_id)
        current_amount = self.amount_total / self.currency_rate if self.currency_rate else self.amount_total
        self.partner_id.commercial_partner_id._check_credit_limit_for_amount(
            self,
            current_amount=current_amount,
        )
        return True

    def action_confirm(self):
        for order in self:
            order.check_limit()
        return super().action_confirm()
