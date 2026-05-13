# See LICENSE file for full copyright and licensing details.
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def check_limit(self):
        self.ensure_one()
        current_amount = self.amount_total
        self.partner_id.commercial_partner_id.with_company(
            self.company_id
        )._check_credit_limit_for_amount(
            self,
            current_amount=current_amount,
        )
        return True

    def action_confirm(self):
        for order in self:
            order.check_limit()
        return super().action_confirm()
