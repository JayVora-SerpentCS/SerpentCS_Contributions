# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import fields, models, api

class project(models.Model):

    _inherit = 'project.project'

    @api.one
    @api.depends('message_ids')
    def _get_recent_date(self):
        date_lst = [x.date for x in self.message_ids]
        self.recent_date = date_lst and max(date_lst) or False

    recent_date = fields.Datetime(compute="_get_recent_date", string="Recent date")
