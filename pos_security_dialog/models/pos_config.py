# -*- coding: utf-8 -*-

from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    enable_security_dialog = fields.Boolean(string="Enable Security Dialog",
                                            default=True)
