odoo.define('import_export_templating.ImportExport', function (require) {
"use strict";

var Bus = require('web.Bus');
var FormController = require('web.FormController');
var ListController = require('web.ListController');
var ActionManager = require('web.ActionManager');
var Dialog = require('web.Dialog');
var dom = require('web.dom');
var core = require('web.core');
var Sidebar = require('web.Sidebar');

var _t = core._t;

FormController.include({
    /**
     * @override
     */
    renderSidebar: function ($node) {
        var self = this;
        if (this.hasSidebar) {
            var otherItems = [];
            if (this.archiveEnabled && this.initialState.data.active !== undefined) {
                var classname = "o_sidebar_item_archive" + (this.initialState.data.active ? "" : " o_hidden")
                otherItems.push({
                    label: _t("Archive"),
                    callback: function () {
                        Dialog.confirm(self, _t("Are you sure that you want to archive this record?"), {
                            confirm_callback: self._toggleArchiveState.bind(self, true),
                        });
                    },
                    classname: classname,
                });
                classname = "o_sidebar_item_unarchive" + (this.initialState.data.active ? " o_hidden" : "")
                otherItems.push({
                    label: _t("Unarchive"),
                    callback: this._toggleArchiveState.bind(this, false),
                    classname: classname,
                });
            }
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
            return this.sidebar.appendTo($node).then(function() {
                 // Show or hide the sidebar according to the view mode
                self._updateSidebar();
            });
        }
        return Promise.resolve();
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
        var self = this;
        if (this.hasSidebar) {
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
                    callback: function () {
                        Dialog.confirm(self, _t("Are you sure that you want to archive all the selected records?"), {
                            confirm_callback: self._toggleArchiveState.bind(self, true),
                        });
                    }
                });
                other.push({
                    label: _t("Unarchive"),
                    callback: this._toggleArchiveState.bind(this, false)
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
            return this.sidebar.appendTo($node).then(function() {
                self._toggleSidebar();
            });
        }
        return Promise.resolve();
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
    /**
     * Executes actions with attribute target='new'. Such actions are rendered
     * in a dialog.
     *
     * @private
     * @param {Object} action
     * @param {Object} options @see doAction for details
     * @returns {Deferred} resolved when the controller is rendered inside a
     *   dialog appended to the DOM
     */
    _executeActionInDialog: function (action, options) {
        var self = this;
        var controller = this.controllers[action.controllerID];
        var widget = controller.widget;

        return this._startController(controller).then(function (controller) {
            var prevDialogOnClose;
            if (self.currentDialogController) {

                if (action.context['nodestroy']) {
                    self.precurrentDialogController = self.currentDialogController;
                    prevDialogOnClose = self.currentDialogController.onClose;
                }else {
                    prevDialogOnClose = self.currentDialogController.onClose;
                    self._closeDialog({ silent: true });
                }
            }

            controller.onClose = prevDialogOnClose || options.on_close;
            var dialog = new Dialog(self, _.defaults({}, options, {
                buttons: [],
                dialogClass: controller.className,
                title: action.name,
                size: action.context.dialog_size,
            }));
            /**
             * @param {Object} [options={}]
             * @param {Object} [options.infos] if provided and `silent` is
             *   unset, the `on_close` handler will pass this information,
             *   which gives some context for closing this dialog.
             * @param {boolean} [options.silent=false] if set, do not call the
             *   `on_close` handler.
             */
            dialog.on('closed', self, function (options) {
                options = options || {};
                self._removeAction(action.jsID);
                self.currentDialogController = null;
                if (options.silent !== true) {
                    controller.onClose(options.infos);
                }
            });
            controller.dialog = dialog;

            return dialog.open().opened(function () {
                self.currentDialogController = controller;

                dom.append(dialog.$el, widget.$el, {
                    in_DOM: true,
                    callbacks: [{widget: dialog}, {widget: controller.widget}],
                });
                widget.renderButtons(dialog.$footer);
                dialog.rebindButtonBehavior();

                return action;
            });
        }).guardedCatch(function () {
            self._removeAction(action.jsID);
        });
    },

    _executeCloseAction: function (action, options) {
        var result;
        if (!this.currentDialogController) {
            result = options.on_close(action.infos);
            if(action && action.context && action.context.close_previous_dialog){
                if(this.precurrentDialogController){
                    if (this.precurrentDialogController) {
                        this.precurrentDialogController.dialog.destroy(options);
                        this.precurrentDialogController = null;
                    }
                }
            }
        }

        this._closeDialog({ infos: action.infos });

        // display some effect (like rainbowman) on appropriate actions
        if (action.effect) {
            this.trigger_up('show_effect', action.effect);
        }

        return Promise.resolve(result);
    },

});

});
