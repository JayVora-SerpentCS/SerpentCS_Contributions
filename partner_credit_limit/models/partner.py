# See LICENSE file for full copyright and licensing details.

from odoo import _, fields, models
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    over_credit = fields.Boolean(
        "Allow Over Credit?",
        help="Allow this commercial customer's sales orders and customer invoices "
        "to exceed the credit limit. This applies across companies.",
    )

    def _check_credit_limit_for_amount(
        self, record, current_amount=0.0, exclude_amount=0.0
    ):
        self.ensure_one()
        record = record.with_company(record.company_id)
        commercial_partner = self.commercial_partner_id

        if (
            commercial_partner.over_credit
            or not record.company_id.account_use_credit_limit
        ):
            return

        # Both native balances are non-stored. Refresh them for successive
        # confirmations/postings in the same transaction.
        commercial_partner.invalidate_recordset(["credit", "credit_to_invoice"])

        # Match the standard sale warning: salespeople may confirm quotations
        # without having read access to the partner's accounting fields.
        warning = (
            self.env["account.move"]
            .with_company(record.company_id)
            ._build_credit_warning_message(
                record.sudo(),
                current_amount=current_amount,
                exclude_amount=exclude_amount,
            )
        )
        if warning:
            raise UserError(
                _(
                    '%(warning)s\nPlease review "%(partner)s" account or credit '
                    "limit settings, or enable Allow Over Credit on the customer.",
                    warning=warning,
                    partner=commercial_partner.display_name,
                )
            )
