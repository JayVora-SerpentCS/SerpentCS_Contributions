# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import fields, models, api


class Project(models.Model):

    _inherit = 'project.project'

    @api.depends('message_ids')
    def _compute_get_recent_date(self):
        for rec in self:
            date_lst = [x.date for x in rec.message_ids]
            rec.recent_date = date_lst and max(date_lst) or False

    recent_date = fields.Datetime(compute="_compute_get_recent_date",
                                  string="Recent date")
