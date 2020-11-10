# Copyright 2016 Serpent Consulting Services Pvt. Ltd
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import http
from odoo.http import request


class WebFieldData(http.Controller):
    @http.route(["/web/fetch_x2m_data"], type="json", auth="public")
    def get_o2x_data(self, **kwargs):
        o2x_records = kwargs.get("o2x_records")
        o2x_record_datas = kwargs.get("o2x_record_data")
        o2x_datas = []
        for idx, record in enumerate(o2x_records):
            o2x_model = record.get("relation", False)
            o2x_ids = record.get("raw_value", False)
            if o2x_model:
                o2x_obj = request.env[o2x_model]
                all_real = all([isinstance(x, int) for x in o2x_ids])
                all_virt = not any([isinstance(x, int) for x in o2x_ids])
                if all_real:
                    o2x_datas.append(o2x_obj.search_read([("id", "in", o2x_ids)]))
                elif all_virt:
                    o2x_datas.append([x["data"] for x in o2x_record_datas[idx]["data"]])
                else:
                    o2x_datas.append([])
                    for item in o2x_record_datas[idx]["data"]:
                        if isinstance(item["data"].get("id"), int):
                            o2x_datas[-1].append(o2x_obj.search_read([("id", "=", item["data"]["id"])]))
                        else:
                            o2x_datas[-1].append(item["data"])
        return o2x_datas
