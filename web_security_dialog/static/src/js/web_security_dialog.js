odoo.define("web_security_dialog.SecurityDialog",function(require){
    "use strict";

    var core = require('web.core');
    var FormController = require('web.FormController');
    var Dialog = require('web.Dialog');
    var rpc = require('web.rpc');
    var session = require('web.session');
    var framework = require('web.framework');

    var QWeb = core.qweb;
    var _t = core._t;

    FormController.include({
        _onButtonClicked: function (event) {
            // stop the event's propagation as a form controller might have other
            // form controllers in its descendants (e.g. in a FormViewDialog)
            event.stopPropagation();
            var self = this;

            this._disableButtons();

            var attrs = event.data.attrs;
            this.is_dialog_security = false;
            if(attrs.options){
                this.is_dialog_security = attrs.options.security
                        ? attrs.options.security
                        : false;
            }

            function saveAndExecuteAction () {
                return self.saveRecord(self.handle, {
                    stayInEdit: true,
                }).then(function () {
                    // we need to reget the record to make sure we have changes made
                    // by the basic model, such as the new res_id, if the record is
                    // new.
                    var record = self.model.get(event.data.record.id);
                    return self._callButtonAction(attrs, record);
                });
            }

            function openmodel_dialog(){
                return $.when(self.open_pincode_dialog()).done(function(dialog){
                    dialog.$footer.find('.validate_pincode').click(function(){
                        var password = dialog.$el.find("#pincode").val();
                        if (password) {
                            framework.blockUI();
                            var callback = self.validate_pincode(self.is_dialog_security,password);
                            callback.done(function(result){
                                framework.unblockUI();
                                if (result) {
                                    dialog.close();
                                    saveAndExecuteAction(event);
                                } else {
                                    Dialog.alert(self, _t("Invalid or Wrong Password! Contact your Administrator."));
                                    return;
                                }
                            }).fail(function(error){
                                framework.unblockUI();
                                Dialog.alert(self, _t("Either the password is wrong or the connection is lost! Contact your Administrator."));
                                return;
                            });
                        } else {
                            Dialog.alert(self, _t("Please Enter the Password."));
                            return;
                        }
                    });
                });
            }
            var d = $.Deferred();
            var def = d.promise();
            if (attrs.confirm && self.is_dialog_security) {
                Dialog.confirm(this, attrs.confirm, {
                    confirm_callback: openmodel_dialog,
                }).on("closed", null, function (){
                    d.resolve();
                });
            } else if (attrs.confirm && !self.is_dialog_security) {
                Dialog.confirm(this, attrs.confirm, {
                    confirm_callback: saveAndExecuteAction,
                }).on("closed", null, function () {
                    d.resolve();
                });
                def = d.promise();
            } else if (attrs.special === 'cancel') {
                def = this._callButtonAction(attrs, event.data.record);
            } else if (!attrs.special || attrs.special === 'save') {
                // save the record but don't switch to readonly mode
                def = saveAndExecuteAction();
            }

            def.always(this._enableButtons.bind(this));
        },
        open_pincode_dialog : function(event){
            var self = this;
            return new Dialog(self,{
                title: _t('Security'),
                size : "small",
                $content: QWeb.render('DialogSecurity'),
                buttons: [
                            {
                                text: _t("Ok"),
                                classes: 'btn-primary validate_pincode',
                            },
                            {
                                text:_t('Cancel'),
                                close:true
                            }
                        ]
            }).open();
        },
        validate_pincode : function(field,value) {
            var self = this;
            var data = false;
            var data_vals = {
                    "field" : field,
                    "password"  : value,
                    "companyId" : session.company_id
                };
           var data_value = rpc.query({
                model: 'res.company',
                method: 'check_security',
                args: [[],data_vals]
            }).then(function (result) {
                    return result;
            });
            return data_value;
        }
    });

});

