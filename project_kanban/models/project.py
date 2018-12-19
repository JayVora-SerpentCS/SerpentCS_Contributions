# Copyright 2016 Serpent Consulting Services Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Project(models.Model):
    _inherit = 'project.project'

    @api.depends('message_ids')
    def _compute_get_recent_date(self):
        for project in self:
            # TODO: It can be improved using tasks of the projects
            # instead of message_ids
            date_lst = [x.date for x in project.message_ids]
            project.recent_date = date_lst and max(date_lst) or False

    recent_date = fields.Datetime(
        compute="_compute_get_recent_date",
        string="Recent date",
        help="This will be auto set"
    )
