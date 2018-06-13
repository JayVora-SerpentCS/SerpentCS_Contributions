odoo.define('import_export_templating.ImportExport', function (require) {
"use strict";

var Bus = require('web.Bus');
var FormController = require('web.FormController');
var ListController = require('web.ListController');
var ActionManager = require('web.ActionManager');
var Dialog = require('web.Dialog');
var ViewManager = require('web.ViewManager');
var dom = require('web.dom');
var core = require('web.core');
var Sidebar = require('web.Sidebar');

var _t = core._t;

FormController.include({
    /**
     * @override
     */
    renderSidebar: function ($node) {
        if (!this.sidebar && this.hasSidebar) {
            var otherItems = [];
            if (this.is_action_enabled('delete')) {
                otherItems.push({
                    label: _t('Delete'),
                    callback: this._onDeleteRecord.bind(this),
                });
            }
            if (this.is_action_enabled('create') && this.is_action_enabled('duplicate')) {
                otherItems.push({
                    label: _t('Duplicate'),
                    callback: this._onDuplicateRecord.bind(this),
                });
            }
            otherItems.push({
                label: _t('Import / Export Tools'),
                callback: this._onActionCall.bind(this),
            });
            this.sidebar = new Sidebar(this, {
                editable: this.is_action_enabled('edit'),
                viewType: 'form',
                env: {
                    context: this.model.get(this.handle).getContext(),
                    activeIds: this.getSelectedIds(),
                    model: this.modelName,
                },
                actions: _.extend(this.toolbarActions, {other: otherItems}),
            });
            this.sidebar.appendTo($node);

            // Show or hide the sidebar according to the view mode
            this._updateSidebar();
        }
    },

    _onActionCall: function (event) {
        this.do_action({
            name:'Import / Export Tools',
            type: 'ir.actions.act_window',
            res_model: 'wiz.download.template',
            views: [[false, 'form']],
            context: {'active_model':this.modelName, 'nodestroy': true},
            target: 'new'
        });
    },    

});


ListController.include({
    /**
     * @override
     */
    renderSidebar: function ($node) {
        if (this.hasSidebar && !this.sidebar) {
            var other = [{
                label: _t("Export"),
                callback: this._onExportData.bind(this)
            }];

            other.push({
                label: _t('Import / Export Tools'),
                callback: this._onActionCall.bind(this),
            });

            if (this.archiveEnabled) {
                other.push({
                    label: _t("Archive"),
                    callback: this._onToggleArchiveState.bind(this, true)
                });
                other.push({
                    label: _t("Unarchive"),
                    callback: this._onToggleArchiveState.bind(this, false)
                });
            }
            if (this.is_action_enabled('delete')) {
                other.push({
                    label: _t('Delete'),
                    callback: this._onDeleteSelectedRecords.bind(this)
                });
            }
            this.sidebar = new Sidebar(this, {
                editable: this.is_action_enabled('edit'),
                env: {
                    context: this.model.get(this.handle, {raw: true}).getContext(),
                    activeIds: this.getSelectedIds(),
                    model: this.modelName,
                },
                actions: _.extend(this.toolbarActions, {other: other}),
            });
            this.sidebar.appendTo($node);

            this._toggleSidebar();
        }
    },

    _onActionCall: function (event) {
        this.do_action({
            name:'Import / Export Tools',
            type: 'ir.actions.act_window',
            res_model: 'wiz.download.template',
            views: [[false, 'form']],
            context: {'active_model':this.modelName, 'nodestroy': true},
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
                
                this.dialog = new Dialog(this, _.defaults(options || {}, {
                    title: executor.action.name,
                    dialogClass: executor.klass,
                    buttons: [],
                    size: executor.action.context.dialog_size,
                }));

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
                var $dialogFooter;
                if (this.dialog_widget instanceof ViewManager) {
                    executor.action.viewManager = this.dialog_widget;
                    $dialogFooter = $('<div/>'); // fake dialog footer in which view
                                                 // manager buttons will be put
                    _.defaults(this.dialog_widget.flags, {
                        $buttons: $dialogFooter,
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
                return this.dialog_widget.appendTo(fragment).then(function () {
                    var def = $.Deferred();
                    self.dialog.opened().then(function () {
                        dom.append(self.dialog.$el, fragment, {
                            in_DOM: true,
                            callbacks: [{widget: self.dialog_widget}],
                        });
                        if ($dialogFooter) {
                            self.dialog.$footer.empty().append($dialogFooter.contents());
                        }
                        if (options.state && self.dialog_widget.do_load_state) {
                            return self.dialog_widget.do_load_state(options.state);
                        }
                    })
                    .done(def.resolve.bind(def))
                    .fail(def.reject.bind(def));
                    self.dialog.open();
                    return def;
                }).then(function () {
                    return executor.action;
                });
            }
            var def = this.inner_action && this.webclient && this.webclient.clear_uncommitted_changes() || $.when();
            return def.then(function() {
                self.dialog_stop(executor.action);
                return self.push_action(executor.action.viewManager = executor.widget(), executor.action, options).then(function () {
                    return executor.action;
                });
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
        
        // Display rainbowman on appropriate actions
        if (action.effect) {
            this.trigger_up('show_effect', action.effect);
        }

        return $.when();
    },

});


});
