odoo.define("web_security_dialog.SecurityDialog",function(require){
    "use strict";

    var core = require('web.core');
    var FromWidget = require('web.form_widgets');
    var Dialog = require('web.Dialog');
    var Model = require('web.DataModel');
    var framework = require('web.framework');

    var QWeb = core.qweb;
    var _t = core._t;

    FromWidget.WidgetButton.include({
        init : function(field_manager, node) {
            this._super(field_manager, node);
            if(this.node.attrs.options) {
                this.options = JSON.parse(this.node.attrs.options)
                    ? JSON.parse(this.node.attrs.options)
                            : false;
                if(this.options) {
                    this.is_dialog_security = this.options.security
                    ? this.options.security
                            : false;
                }else{
                    this.is_dialog_security = false;
                }
            }
        },
        on_click : function() {
            var self = this;
            if (this.view.is_disabled) {
                return;
            }
            self.view.enable_button();
            self.force_disabled = false;
            self.check_disable();
            if (self.$el.hasClass('o_wow')) {
                self.show_wow();
            }
            if (this.is_dialog_security) {
                self.dialog = new Dialog(self,{
                    title: _t('Security'),
                    size : "small",
                    $content: QWeb.render('DialogSecurity'),
                    buttons: [
                                {
                                    text:_t('Cancel'),
                                    close:true
                                },
                                {
                                    text: _t("Ok"),
                                    click: function(){
                                       var curr_obj = this;
                                       var pass_value = this.$el.find("#d_security").val();
                                       if (pass_value) {
                                           framework.blockUI();
                                           var callback = self.validate_user(self.is_dialog_security,pass_value);
                                           callback.done(function(result) {
                                               framework.unblockUI();
                                               if (result) {
                                                   curr_obj.close();
                                                   self.click_operation();
                                               }else {
                                                   Dialog.alert(self, _t("Password is Wrong"));
                                                   return;
                                               }
                                           }).fail(function(error) {
                                               framework.unblockUI();
                                               Dialog.alert(self, _t("Connection lost"));
                                               return;
                                           });
                                       }else {
                                           Dialog.alert(self, _t("Please Enter the Password."));
                                           return;
                                       }
                                    }
                                }
                            ]
                }).open();
            }else {
            self.click_operation();
            }
        },
        click_operation : function() {
            var self = this;
            this.execute_action().always(function() {
                self.view.enable_button();
                self.force_disabled = false;
                self.check_disable();
                if (self.$el.hasClass('o_wow')) {
                    self.show_wow();
                }
            });
        },
        validate_user : function(field,value) {
            var self = this;
            var data_vals = {
                    "field" : field,
                    "password"  : value,
                    "userId" : self.session.uid
                };
          return new Model("res.users").call("check_security",[[],data_vals]);
        }
    });

});

