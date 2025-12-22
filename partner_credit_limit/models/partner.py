# See LICENSE file for full copyright and licensing details.

from odoo import fields, models,api,_
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    over_credit = fields.Boolean('Allow Over Credit?')
    Available_credit = fields.Float(
        string="Available Credit Limit", compute="_compute_available_credit", store=True)

    @api.depends('credit_limit', 'credit', 'debit', 'sale_order_ids', 'sale_order_ids.state')
    def _compute_available_credit(self):
        for partner in self:
            moveline_obj = self.env['account.move.line']
            movelines = moveline_obj.search([
                ('partner_id', '=', partner.id),
                ('account_id.account_type', 'in', ['Receivable', 'Payable']),
                ('move_id.state', '!=', 'cancel')
            ])
            credit = sum(movelines.mapped('credit'))
            debit = sum(movelines.mapped('debit'))

            confirm_sale_orders = self.env['sale.order'].search([
                ('partner_id', '=', partner.id),
                ('state', '=', 'sale'),
                ('invoice_status', '!=', 'invoiced')
            ])
            amount_total = sum(confirm_sale_orders.mapped('amount_total'))

            partner_credit_limit = (debit + amount_total) - credit
            available_credit = partner.credit_limit - partner_credit_limit
            partner.Available_credit = max(available_credit, 0.0)

    @api.constrains('credit_limit')
    def check_nagative_value_in_credit_limit(self):
        for record in self:
            if record.credit_limit < 0:
                raise ValidationError(_("Credit Limit Should Be Positive Value."))

    def _inverse_use_partner_credit_limit(self):
        company_limit = self._fields['credit_limit'].get_company_dependent_fallback(self)
        for partner in self:
            if not partner.use_partner_credit_limit:
                if partner.credit_limit and partner.credit_limit != 0:
                    continue
                partner.credit_limit = company_limit

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    @api.constrains('account_default_credit_limit')
    def check_nagative_value_in_account_default_credit_limit(self):
        for record in self:
            if record.account_default_credit_limit < 0:
                raise ValidationError(_("Account Default Credit Limit Should Be Positive Value."))