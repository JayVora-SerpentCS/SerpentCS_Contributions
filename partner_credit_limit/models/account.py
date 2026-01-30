from odoo import models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    def action_post(self):
        res = super(AccountPayment, self).action_post()
        for payment in self:
            partner = payment.partner_id
            if partner and payment.amount:
                partner._compute_available_credit()
        return res