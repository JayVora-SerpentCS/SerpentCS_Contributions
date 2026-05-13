from odoo import models

class AccountMove(models.Model):
    _inherit = "account.move"

    def check_credit_limit(self):
        for move in self:
            if move.move_type != "out_invoice":
                continue

            move.with_company(move.company_id)
            total_field = (
                "total_amount_currency"
                if move.currency_id == move.company_currency_id
                else "total_amount"
            )
            current_amount = move.tax_totals[total_field]
            move.partner_id.commercial_partner_id._check_credit_limit_for_amount(
                move,
                current_amount=current_amount,
                exclude_amount=move._get_partner_credit_warning_exclude_amount(),
            )

    def action_post(self):
        for invoice in self:
            invoice.check_credit_limit()
        return super().action_post()
