odoo.define('import_export_templating.ImportExport', function (require) {
"use strict";

var Bus = require('web.Bus');
var FormView = require('web.FormView')
var ListView = require('web.ListView')
var ActionManager = require('web.ActionManager');
var Dialog = require('web.Dialog');
var ViewManager = require('web.ViewManager');
var core = require('web.core');
var Sidebar = require('web.Sidebar');

var _t = core._t;

FormView.include({
    /**
     * @override
     */
	render_sidebar: function($node) {
        if (!this.sidebar && this.options.sidebar) {
            this.sidebar = new Sidebar(this, {editable: this.is_action_enabled('edit')});
            if (this.fields_view.toolbar) {
                this.sidebar.add_toolbar(this.fields_view.toolbar);
            }
            var canDuplicate = this.is_action_enabled('create') && this.is_action_enabled('duplicate');
            this.sidebar.add_items('other', _.compact([
                this.is_action_enabled('delete') && { label: _t('Delete'), callback: this.on_button_delete },
                canDuplicate && { label: _t('Duplicate'), callback: this.on_button_duplicate },
                {label: _t('Import / Export Tools'),callback:this._onActionCall.bind(this)}
            ]));

            this.sidebar.add_items()
            this.sidebar.appendTo($node);

            // Show or hide the sidebar according to the view mode
            this.toggle_sidebar();
        }
    },

    _onActionCall: function (event) {
        this.do_action({
            name:'Import / Export Tools',
            type: 'ir.actions.act_window',
            res_model: 'wiz.download.template',
            views: [[false, 'form']],
            context: {'active_model':this.model, 'nodestroy': true},
            target: 'new'
        });
    },

});


ListView.include({
    /**
     * @override
     */
	render_sidebar: function($node) {
        if (!this.sidebar && this.options.sidebar) {
            this.sidebar = new Sidebar(this, {editable: this.is_action_enabled('edit')});
            if (this.fields_view.toolbar) {
                this.sidebar.add_toolbar(this.fields_view.toolbar);
            }
            this.sidebar.add_items('other', _.compact([
                { label: _t("Export"), callback: this.on_sidebar_export },
                this.fields_view.fields.active && {label: _t("Archive"), callback: this.do_archive_selected},
                this.fields_view.fields.active && {label: _t("Unarchive"), callback: this.do_unarchive_selected},
                this.is_action_enabled('delete') && { label: _t('Delete'), callback: this.do_delete_selected },
                {label: _t('Import / Export Tools'), callback: this._onActionCall.bind(this),}
            ]));

            $node = $node || this.options.$sidebar;
            this.sidebar.appendTo($node);

            // Hide the sidebar by default (it will be shown as soon as a record is selected)
            this.sidebar.do_hide();
        }
    },

    _onActionCall: function (event) {
        this.do_action({
            name:'Import / Export Tools',
            type: 'ir.actions.act_window',
            res_model: 'wiz.download.template',
            views: [[false, 'form']],
            context: {'active_model':this.model, 'nodestroy': true},
            target: 'new'
        });
    },

});


ActionManager.include({

	ir_actions_common: function(executor, options) {
        var self = this;
        if (executor.action.target === 'new') {
            var pre_dialog = (this.dialog && !this.dialog.isDestroyed()) ? this.dialog : null;
            var flag = true;
            if (pre_dialog){
                // prevent previous dialog to consider itself closed,
                // right now, as we're opening a new one (prevents
                // reload of original form view)
                pre_dialog.off('closed', null, pre_dialog.on_close);
            }
            if (this.dialog_widget && !this.dialog_widget.isDestroyed()) {
                if(executor.action && executor.action.context  &&
                    executor.action.context['nodestroy']){
                    flag = false;
                    self.prev_dialog = self.dialog
                    self.prev_dialog_widget = self.dialog_widget
                }else{
                    this.dialog_widget.destroy();
                }
            }
            // explicitly passing a closing action to dialog_stop() prevents
            // it from reloading the original form view
            if(flag){
                this.dialog_stop(executor.action);
            }

            // explicitly passing a closing action to dialog_stop() prevents
            // it from reloading the original form view
            this.dialog_stop(executor.action);
            this.dialog = new Dialog(this, {
                title: executor.action.name,
                dialogClass: executor.klass,
                buttons: [],
                size: executor.action.context.dialog_size,
            });

            // chain on_close triggers with previous dialog, if any
            this.dialog.on_close = function(){
                options.on_close.apply(null, arguments);
                if (pre_dialog && pre_dialog.on_close){
                    // no parameter passed to on_close as this will
                    // only be called when the last dialog is truly
                    // closing, and *should* trigger a reload of the
                    // underlying form view (see comments above)
                    pre_dialog.on_close();
                }
                if (!pre_dialog) {
                    self.dialog = null;
                }
            };
            this.dialog.on("closed", null, this.dialog.on_close);
            this.dialog_widget = executor.widget();
            if (this.dialog_widget instanceof ViewManager) {
                _.extend(this.dialog_widget.flags, {
                    $buttons: this.dialog.$footer,
                    footer_to_buttons: true,
                });
                if (this.dialog_widget.action.view_mode === 'form') {
                    this.dialog_widget.flags.headless = true;
                }
            }
            if (this.dialog_widget.need_control_panel) {
                // Set a fake bus to Dialogs needing a ControlPanel as they should not
                // communicate with the main ControlPanel
                this.dialog_widget.set_cp_bus(new Bus());
            }
            this.dialog_widget.setParent(this.dialog);

            var fragment = document.createDocumentFragment();
            return this.dialog_widget.appendTo(fragment).then(function() {
                self.dialog.open().$el.append(fragment);
                if(options.state && self.dialog_widget.do_load_state) {
                    return self.dialog_widget.do_load_state(options.state);
                }
            }).then(function () { return executor.action; });
        }
        var def = this.inner_action && this.webclient && this.webclient.clear_uncommitted_changes() || $.when();
        return def.then(function() {
            self.dialog_stop(executor.action);
            return self.push_action(executor.widget(), executor.action, options);
        }).fail(function() {
            return $.Deferred().reject();
        });
    },
    ir_actions_act_window_close: function (action, options) {
            if (!this.dialog) {
                options.on_close();
            }
            if(action && action.context && action.context.close_previous_dialog){
                if(this.prev_dialog){
                    this.prev_dialog_widget.destroy()
                    this.prev_dialog.destroy()
                    this.prev_dialog = null
                }
                if(this.dialog){
                    this.dialog_stop();
                }
            }else{
                this.dialog_stop();
            }
            return $.when();
        },
});


});
