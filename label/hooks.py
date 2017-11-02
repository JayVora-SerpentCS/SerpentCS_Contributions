# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.


def uninstall_hook(cr, registry):
    cr.execute("select id,ref_ir_act_report,ref_ir_value from label_print")
    label_data = cr.fetchall()
    if label_data:
        act_list = []
        value_list = []
        for rec in label_data:
            act_list.append(rec[1])
            value_list.append(rec[2])
        cr.execute("delete from ir_act_window where id in %s",
                   (tuple(act_list),))
        cr.execute("delete from ir_values where id in %s",
                   (tuple(value_list),))
