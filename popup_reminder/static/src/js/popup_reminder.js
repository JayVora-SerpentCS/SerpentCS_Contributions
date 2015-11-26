odoo.define('popup_reminder.popup_reminder', function (require) {
        "use strict";
    var core = require('web.core');
    var Model = require('web.DataModel');
    var WebClient = require('web.WebClient');
    var session = require('web.session');
    var bus = require('bus.bus')

    var _t = core._t;
    var QWeb = core.qweb;

    WebClient.include({
        init: function(parent, client_options) {
            this._super(parent);
            this._logged_in = null;
            this.showOrHide = true;
            this.length = 0;
        },
        start: function() {
            var self = this;
            return $.when(this._super()).then(function() {
                self.bus = bus.bus
                self.bus.on("notification", self, self.on_notification);
            })
        },
        bind_hashchange: function() {
            var self = this;
            $(window).bind('hashchange', this.on_hashchange);

            var state = $.bbq.getState(true);
            if (_.isEmpty(state) || state.action == "login") {
                self._logged_in = true;
                self.bind_events()
                self.menu.is_bound.done(function() {
                    new Model("res.users").call("read", [session.uid, ["action_id"]]).done(function(data) {
                        if(data.action_id) {
                            self.action_manager.do_action(data.action_id[0]);
                            self.menu.open_action(data.action_id[0]);
                        } else {
                            var first_menu_id = self.menu.$el.find("a:first").data("menu");
                            if(first_menu_id) {
                                self.menu.menu_click(first_menu_id);
                            }                    }
                    });
                });
            } else {
                $(window).trigger('hashchange');
            }
        },
        bind_events: function(){
            var self = this;
            this._super.apply(this, arguments);
            $('.oe_popuptray').show();
            $('.oe_popup0').remove()
            var $icon = $(QWeb.render('oe_popup'));
            self.popup_reminder_data = ''
            self.record_header = ''
            self.popup_value = ''
            self.color_list = []
            self.unique_list = []
            self.get_popupdata()
            $icon.on('click', function() {
                self.get_popupdata()
                $.when(self.get_popupdata()).done(function() {
                    $( "#popup").toggle( self.showOrHide );
                    self.$el.find(".oe_popup_notification").removeClass('oe_highlight_btn')
                    if ( self.showOrHide) {
                        $( "#popup" ).show();
                        if(self.length){
                            $('#oe_main_menu_navbar', self.$el).append(QWeb.render('popup-reminder-view',{widget:self, popup_reminder_data: self.popup_reminder_data, record_header: self.record_header}));
                        }
                        self.showOrHide = false
                    } else if ( !self.showOrHide) {
                        $( "#popup" ).hide();
                        self.$el.find('#popup').remove()
                        self.showOrHide = true
                    }
                    self.get_data()
                })
            });
            $icon.prependTo(window.$('.oe_popuptray'));
            if(self._logged_in){
                self._logged_in = false;
                return $.when(self.get_popupdata()).done(function() {
                    $icon.click()
                })
            }
        },
        on_notification: function(notification) {
            var self = this;
            var channel = notification[0];
            var message = notification[1];

            if((Array.isArray(channel) && (channel[1] === 'popup.reminder'))){
                if(message){
                    if(!self.showOrHide){
                        $( "#popup" ).hide();
                        self.$el.find('#popup').remove()
                        self.showOrHide = true
                    }
                    return $.when(self.get_popupdata()).done(function() {
                        self.$el.find(".oe_popup_notification").addClass('oe_highlight_btn')
                    })
                }else{
                    self.$el.find(".oe_popup_notification").text(message)
                }
            }
        },
        get_data: function(){
            var self = this
            $('#oe_main_menu_navbar').find('.oe_popup_header_click').on('click', function(e) {
                var form_ids = self.alive(new Model('popup.reminder').call('get_model_name',[e.currentTarget.attributes.value.value]));
                form_ids.then(function(response) {
                    self.action_manager.do_action({
                        name: response[0],
                        res_model: response[1],
                        type: 'ir.actions.act_window',
                        view_type : 'list',
                        view_mode : 'list',
                        views: [[false, 'list'], [false, 'form']],
                        target: 'current'
                    });
                })
            });
            $('#oe_main_menu_navbar').find('.oe_popup_record_click').on('click', function(e) {
                var btn_txt = e.currentTarget.attributes.value.value
                var btn_data = btn_txt.split('//')
                var form_ids = self.alive(new Model('popup.reminder').call('get_form_data',[btn_data[0]]));
                form_ids.then(function(response) {
                    self.action_manager.do_action({
                        res_model: response,
                        type: 'ir.actions.act_window',
                        res_id: parseInt(btn_data[1]),
                        view_type : 'form',
                        view_mode : 'form',
                        views: [[false, 'form']],
                        target: 'current'
                    });
                })
            });
        },
        get_popupdata: function(){
            var self = this;
            var record_header_data = self.alive(new Model("popup.reminder").call("set_record_header"));
            record_header_data.then(function(header) {
                self.record_header = header
            })
            var unique_id_data = self.alive(new Model('popup.reminder').call('get_unique_id'));
            unique_id_data.then(function(unique) {
                self.unique_list.push(unique)
            })
            var reminder_data = self.alive(new Model("popup.reminder").call("set_notification",[false]));
            reminder_data.then(function(response) {
                self.popup_reminder_data = response
                self.length = 0
                $.each(self.popup_reminder_data, function(key, value) {
                    var color_data = self.alive(new Model('popup.reminder').call('get_color_name',[key]));
                    color_data.then(function(response) {
                        self.color_list.push(response)
                        _.each(response, function(k, v){
                            if (key == v){
                                var unique_id = ''
                                _.each(self.unique_list, function(unique_key, unique_value){
                                    _.each(unique_key, function(kk,vv){
                                        if (vv == key){
                                            self.$el.find("#popup .oe_popup_list #" + kk +" ").css({'background-color': k});
                                        }
                                    })
                                })
                            }
                        })
                    })
                    $.each(value, function(v) {
                        self.length += 1
                    });
                });
            }).done(function() {
                self.$el.find(".oe_popup_notification").text(self.length)
            })
            return $.when(record_header_data, unique_id_data, reminder_data)
        },
        get_unique_id: function(header){
            var self = this;
            var unique_id = ''
            _.each(self.unique_list, function(key, value){
                _.each(key, function(k,v){
                    if (v == header){
                        unique_id = k
                    }
                })
            })
            return unique_id
        },
        get_color_name: function(recod_name){
            var self = this;
            self.color = ''
            _.each(self.color_list, function(data){
                _.each(data, function(key, value){
                    if (value.toString() == recod_name.toString()){
                        self.color = key.toString()
                    }
                })
            })
            return self.color
        },
    });
});