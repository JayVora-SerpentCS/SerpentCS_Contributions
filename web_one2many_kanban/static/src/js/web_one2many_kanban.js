/*global session*/
odoo.define('web_one2many_kanban.web_one2many_kanban', function(require) {
"use strict";

var session = require('web.session');

var core = require('web.core');
var KanbanRecord = require('web.KanbanRecord');
var QWeb = require('web.QWeb');
var rpc = require("web.rpc");
var _t = core._t;


KanbanRecord.include({
    _render: function () {
        var def = $.Deferred();
        var self = this;
        var field_mode = '';
        var field_name = '';
        _.each(this.fieldsInfo, function (field_info, field_nm){
            if(field_info.mode === 'list'){
                field_mode = field_info.mode;
                field_name = field_nm
            }
        })
        if( field_mode === 'list'){
            var record = this.qweb_context.record[field_name]
            if(record.type === 'one2many'){
                var field_record = [];
                def = rpc.query({
                        model: record.relation,
                        method: 'search_read',
                        args: [[['id', 'in', record.raw_value]]],
                    }).then(function(field_records) {
                        _.each(field_records , function (data){
                            field_record.push(data)
                        })
                        record.raw_value = field_record;
                    })
            }
        }
        else{
            def.resolve();
        }
        def.done(function (){
            self.replaceElement(self.qweb.render('kanban-box', self.qweb_context));
            self.$el.addClass('o_kanban_record');
            self.$el.data('record', self);
            if (self.$el.hasClass('oe_kanban_global_click') ||
                self.$el.hasClass('oe_kanban_global_click_edit')) {
                self.$el.on('click', self._onGlobalClick.bind(self));
            }
            self._processFields();
            self._processWidgets();
            self._setupColor();
            self._setupColorPicker();
            self._attachTooltip();

            // We use boostrap tooltips for better and faster display
            self.$('span.o_tag').tooltip({delay: {'show': 50}});
        });
    },
})

});
