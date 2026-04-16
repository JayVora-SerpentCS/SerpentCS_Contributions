# See LICENSE file for full copyright and licensing details.
from odoo import _, api, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def check_limit(self):
        self.ensure_one()
        partner = self.partner_id

        if not partner.use_partner_credit_limit or partner.over_credit:
            return True

        # Skip check for portal users
        user = self.env['res.users'].search(
            [('partner_id', '=', partner.id)], limit=1
        )
        if user and user.has_group('base.group_portal'):
            return True

        movelines = self.env['account.move.line'].search([
            ('partner_id', '=', partner.id),
            ('account_id.account_type', 'in',
             ['asset_receivable', 'liability_payable']),
            ('parent_state', '!=', 'cancel'),
        ])

        confirmed_orders = self.search([
            ('partner_id', '=', partner.id),
            ('state', '=', 'sale'),
            ('invoice_status', '!=', 'invoiced'),
            ('id', '!=', self.id),
        ])

        amount_total = sum(confirmed_orders.mapped('amount_total')) + self.amount_total
        credit = sum(movelines.mapped('credit'))
        debit = sum(movelines.mapped('debit'))

        used_credit = (debit + amount_total) - credit
        available_credit = round(partner.credit_limit - used_credit, 2)

        if used_credit > partner.credit_limit:
            raise UserError(_(
                'You cannot confirm this Sale Order.\n'
                'Available Credit Limit including current order: %(available)s\n'
                'Please review "%(partner)s" account or credit limit settings or Allow Over Credit from Customer Master.',
                available=available_credit,
                partner=partner.name,
            ))
        return True

    def action_confirm(self):
        """Check credit limit before confirming."""
        for order in self:
            order.check_limit()
        return super().action_confirm()
