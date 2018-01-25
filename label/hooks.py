# See LICENSE file for full copyright and licensing details.


def uninstall_hook(cr, registry):
    cr.execute("select ref_ir_act_report from label_print")
    label_data = cr.fetchall()
    if label_data:
        value_list = [rec[0] for rec in label_data]
        cr.execute("delete from ir_act_window where id in %s",
                   (tuple(value_list),))
        cr.execute("delete from ir_actions where id in %s",
                   (tuple(value_list),))
