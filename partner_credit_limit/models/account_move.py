from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def check_credit_limit(self):
        pending_amounts = {}
        for move in self:
            if move.move_type != "out_invoice" or move.state != "draft":
                continue

            move = move.with_company(move.company_id)
            # Use the same tax totals as Odoo 20's native credit warning,
            # including the invoice's exchange rate and company-currency rounding.
            total_field = (
                "total_amount_currency"
                if move.currency_id == move.company_currency_id
                else "total_amount"
            )
            current_amount = move.tax_totals[total_field]
            exclude_amount = move._get_partner_credit_warning_exclude_amount()
            key = (move.company_id.id, move.partner_id.commercial_partner_id.id)
            pending_amount = pending_amounts.get(key, 0.0)
            move.partner_id.commercial_partner_id.with_company(
                move.company_id
            )._check_credit_limit_for_amount(
                move,
                current_amount=current_amount + pending_amount,
                exclude_amount=exclude_amount,
            )
            pending_amounts[key] = pending_amount + current_amount - exclude_amount

    def action_post(self):
        self.check_credit_limit()
        return super().action_post()
