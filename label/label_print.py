# -*- coding: utf-8 -*-

from osv import fields, osv
from tools.translate import _

class label_print(osv.osv):
    _name = "label.print"

    _columns = {
        'name' : fields.char("Name", size=64, required=True, select=1),
        'model_id' : fields.many2one('ir.model', 'Model', required=True, select=1),
        'field_ids' : fields.one2many("label.print.field", 'report_id', 'Fields'),
        'ref_ir_act_report':fields.many2one('ir.actions.act_window', 'Sidebar action', readonly=True,
                                            help="Sidebar action to make this template available on records "
                                                 "of the related document model"),
        'ref_ir_value':fields.many2one('ir.values', 'Sidebar button', readonly=True,
                                       help="Sidebar button to open the sidebar action"),
        'model_list': fields.char('Model List', size=256)
    }
    def onchange_model(self, cr, uid, ids, model_id):
        model_list = ""
        if model_id:
            model_obj = self.pool.get('ir.model')
            model_data = model_obj.browse(cr, uid, model_id)
            model_list = "[" + str(model_id) + ""
            active_model_obj = self.pool.get(model_data.model)
            if active_model_obj._inherits:
                for key, val in active_model_obj._inherits.items():
                    model_ids = model_obj.search(cr, uid, [('model', '=', key)])
                    if model_ids:
                        model_list += "," + str(model_ids[0]) + ""
            model_list += "]"
        return {'value': {'model_list': model_list}}

    def create_action(self, cr, uid, ids, context=None):
        vals = {}
        action_obj = self.pool.get('ir.actions.act_window')
        for data in self.browse(cr, uid, ids, context=context):
            src_obj = data.model_id.model
            button_name = _('Label (%s)') % data.name
            vals['ref_ir_act_report'] = action_obj.create(cr, uid, {
                 'name': button_name,
                 'type': 'ir.actions.act_window',
                 'res_model': 'label.print.wizard',
                 'src_model': src_obj,
                 'view_type': 'form',
                 'context': "{'label_print' : %d}" % (data.id),
                 'view_mode':'form,tree',
                 'target' : 'new',
            }, context)
            vals['ref_ir_value'] = self.pool.get('ir.values').create(cr, uid, {
                 'name': button_name,
                 'model': src_obj,
                 'key2': 'client_action_multi',
                 'value': "ir.actions.act_window," + str(vals['ref_ir_act_report']),
                 'object': True,
             }, context)
        self.write(cr, uid, ids, {
                    'ref_ir_act_report': vals.get('ref_ir_act_report',False),
                    'ref_ir_value': vals.get('ref_ir_value',False),
                }, context)
        return True

    def unlink_action(self, cr, uid, ids, context=None):
        ir_values_obj = self.pool.get('ir.values')
        act_window_obj = self.pool.get('ir.actions.act_window')
        for template in self.browse(cr, uid, ids, context=context):
            try:
                if template.ref_ir_act_report:
                    act_window_obj.unlink(cr, uid, template.ref_ir_act_report.id, context)
                if template.ref_ir_value:
                    ir_values_obj.unlink(cr, uid, template.ref_ir_value.id, context)
            except Exception, e:
                raise osv.except_osv(_("Warning"), _("Deletion of the action record failed. %s" % (e)))
        return True

label_print()

class label_print_field(osv.osv):
    _name = "label.print.field"
    _rec_name = "sequence"
    _order = "sequence"
    _columns = {
        'sequence' : fields.integer("Sequence", required=True),
        'field_id' : fields.many2one('ir.model.fields', 'Fields', required=False),
        'report_id': fields.many2one('label.print', 'Report'),
        'type': fields.selection([('normal','Normal'), ('barcode', 'Barcode'), ('image', 'Image')], 'Type', required=True),
        'python_expression': fields.boolean('Python Expression'),
        'python_field': fields.char('Fields', size=32),
        'fontsize' : fields.float("Font Size"),
        'position' : fields.selection([('left','Left'),('right','Right'),('top','Top'),('bottom','Bottom')],'Position'),
        'nolabel' : fields.boolean('No Label'),
        'newline' : fields.boolean('New Line')
    }

    _defaults = {
        'type': 'normal',
        'fontsize' : 8.0,
        'newline' : True
    }

label_print_field()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
