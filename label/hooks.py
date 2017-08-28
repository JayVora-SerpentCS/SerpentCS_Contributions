# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2017-Today Serpent Consulting Services Pvt. Ltd.
#    (<http://www.serpentcs.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################


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
