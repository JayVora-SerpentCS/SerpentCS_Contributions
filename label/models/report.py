# coding=utf-8

from odoo import models, api

class Report(models.Model):
    _inherit = "report"

    @api.model
    def _get_report_from_name(self, report_name):
        report = super(Report, self)._get_report_from_name(report_name)
        if report:
            paperformat_id = self._context.get('paperformat_id', None)
            if paperformat_id:
                report.paperformat_id = paperformat_id

        return report