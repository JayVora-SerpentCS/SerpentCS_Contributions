# -*- coding: utf-8 -*-
# Author: Guewen Baconnier
# Copyright 2013 Camptocamp SA
# Copyright 2016 Serpent Consulting Services Pvt. Ltd.
# (http://www.serpentcs.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import UserError

QUOTATION_STATES = ['draft', 'sent', 'sale']


class SaleOrderCancel(models.TransientModel):

    """ Ask a reason for the sale order cancellation."""
    _name = 'sale.order.cancel'
    _description = __doc__

    reason_id = fields.Many2one(
        'sale.order.cancel.reason',
        string='Reason',
        required=True)

    @api.multi
    def confirm_cancel(self):
        act_close = {'type': 'ir.actions.act_window_close'}
        sale_ids = self._context.get('active_ids')
        if sale_ids is None:
            return act_close
        assert len(sale_ids) == 1, "Only 1 sale ID expected"
        sale = self.env['sale.order'].browse(sale_ids)
        sale.cancel_reason_id = self.reason_id.id
        if sale.state not in QUOTATION_STATES:
            raise UserError(_('You cannot cancel the Quotation/Order in the '
                              'current state!'))
        sale.action_cancel()
        return act_close
