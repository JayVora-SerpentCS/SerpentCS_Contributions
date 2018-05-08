# -*- coding: utf-8 -*-
# Copyright 2016 Serpent Consulting Services Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class Project(models.Model):
    _inherit = 'project.project'

    @api.multi
    @api.depends('message_ids')
    def _compute_get_recent_date(self):
        for rec in self:
            date_lst = [x.date for x in rec.message_ids]
            rec.recent_date = date_lst and max(date_lst) or False

    recent_date = fields.Datetime(compute="_compute_get_recent_date",
                                  string="Recent date")
