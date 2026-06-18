# See LICENSE file for full copyright and licensing details.


def uninstall_hook(env):
    label_prints = env["label.print"].search(
        [("ref_ir_act_report", "!=", False)]
    )

    if label_prints:
        label_prints.mapped("ref_ir_act_report").unlink()