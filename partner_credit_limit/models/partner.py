# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
from odoo import _, fields, models


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    credit_limit = fields.Float('Credit Limit',
                                help='Credit limit in local amount')
    over_credit = fields.Boolean('Allow Over Credit',
                                 help="Allow to bypass credit for the next operation\
and fix a new credit limit including the next operation amount")
