# -*- coding: utf-8 -*-

from openerp import api, models


class O2mKanbanRecord(models.Model):
    _name = "kanban.record"

    @api.model
    def getKanbanRecord(self, records, o2m_dataset):
        updated_record = []
        for record in records:
            for key, value in o2m_dataset.items():
                ids = record[value["field_name"]]
                res = self.env[value["model"]].browse(ids)
                res_fields = value["fields"]
                o2m_data = res.search_read([('id', 'in', ids)], res_fields)
                record[value["field_name"]] = o2m_data
            updated_record.append(record)
        return updated_record
