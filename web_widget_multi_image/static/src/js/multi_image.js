function openerp_web_widget_multi_image(instance){

    var _t = instance.web._t,
    _lt = instance.web._lt;
    var QWeb = instance.web.qweb;

    instance.web.form.FieldOne2Many = instance.web.form.FieldOne2Many.extend({

        load_views: function() {
            var self = this;
            var modes = this.node.attrs.mode;
            modes = !!modes ? modes.split(",") : ["tree"];
            var views = [];
            _.each(modes, function(mode) {
                if (! _.include(["list", "tree", "graph", "kanban"], mode)) {
                    throw new Error(_.str.sprintf(_t("View type '%s' is not supported in One2Many."), mode));
                }
                var view = {
                    view_id: false,
                    view_type: mode == "tree" ? "list" : mode,
                    options: {}
                };
                if (self.field.views && self.field.views[mode]) {
                    view.embedded_view = self.field.views[mode];
                }
                if(view.view_type === "list") {
                    _.extend(view.options, {
                        addable: null,
                        selectable: self.multi_selection,
                        multi_image : (self.node.attrs.widget == _t('image_multi')) ? true : false,
                        sortable: true,
                        import_enabled: false,
                        deletable: true
                    });
                    if (self.get("effective_readonly")) {
                        _.extend(view.options, {
                            deletable: null,
                            reorderable: false,
                            multi_image : (self.node.attrs.widget == _t('image_multi')) ? true : false
                        });
                    }
                } else if (view.view_type === "form") {
                    if (self.get("effective_readonly")) {
                        view.view_type = 'form';
                    }
                    _.extend(view.options, {
                        not_interactible_on_create: true,
                    });
                } else if (view.view_type === "kanban") {
                    _.extend(view.options, {
                        confirm_on_delete: false,
                    });
                    if (self.get("effective_readonly")) {
                        _.extend(view.options, {
                            action_buttons: false,
                            quick_creatable: false,
                            creatable: false,
                            read_only_mode: true,
                        });
                    }
                }
                views.push(view);
            });
            this.views = views;
            
            this.viewmanager = new instance.web.form.One2ManyViewManager(this, this.dataset, views, {});
            this.viewmanager.o2m = self;
            var once = $.Deferred().done(function() {
                self.init_form_last_update.resolve();
            });
            var def = $.Deferred().done(function() {
                self.initial_is_loaded.resolve();
            });
            this.viewmanager.on("controller_inited", self, function(view_type, controller) {
                controller.o2m = self;
                if (view_type == "list") {
                    if (self.get("effective_readonly")) {
                        controller.on('edit:before', self, function (e) {
                            e.cancel = true;
                        });
                        _(controller.columns).find(function (column) {
                            if (!(column instanceof instance.web.list.Handle)) {
                                return false;
                            }
                            column.modifiers.invisible = true;
                            return true;
                        });
                    }
                } else if (view_type === "form") {
                    if (self.get("effective_readonly")) {
                        $(".oe_form_buttons", controller.$el).children().remove();
                    }
                    controller.on("load_record", self, function(){
                         once.resolve();
                     });
                    controller.on('pager_action_executed',self,self.save_any_view);
                } else if (view_type == "graph") {
                    self.reload_current_view();
                }
                def.resolve();
            });
            this.viewmanager.on("switch_mode", self, function(n_mode, b, c, d, e) {
                $.when(self.save_any_view()).done(function() {
                    if (n_mode === "list") {
                        $.async_when().done(function() {
                            self.reload_current_view();
                        });
                    }
                });
            });
            $.async_when().done(function () {
                self.viewmanager.appendTo(self.$el);
            });
            return def;
        },

    });

    instance.web.ListView.include({

        load_list: function(data) {
            var self = this;
            this._super(data);
            this.$el.find('.oe-image-preview').click(function(){
                var url_list = [];
                var model = self.dataset.model
                self.images_list = [];
                self.image_dataset = new instance.web.DataSetSearch(self, self.model, {}, [] );
                self.image_dataset.read_slice([], {'domain': [['id', '=', self.dataset.ids]]}).done(function(records){
                    self.images_list = records
                    var images_list = self.images_list;
                    if (images_list && !_.isEmpty(images_list)) {
                        _.each(images_list, function(img) {
                            if (img) {
                                var src=window.location.origin + "/web/binary/image?model=" + model + "&field=image&id="+img.id
                                if(img.image){
                                    var src="data:image/jpeg;base64,"+img.image
                                }
                                var title = img['title'] ? img['title'] : ''
                                    var description = img['description'] ? img['description'] : ''
                                    url_list.push({
                                        "url": src,
                                        "title": 'Title:-' + title + '<br/>Description:-' + description
                                    });
                            }
                        });
                    } else {
                        self.do_warn("Image", "Image not available !");
                        return false;
                    }
                    self.$el.find('.oe-image-preview').lightbox({
                        fitToScreen: true,
                        jsonData: url_list,
                        loopImages: true,
                        imageClickClose: false,
                        disableNavbarLinks: true
                    });
                });
            });
            
            this.$el.find('.oe_image_list').click(function(){
                self.images_list = [];
                self.image_dataset = new instance.web.DataSetSearch(self, self.model, {}, [] );
                self.image_dataset.read_slice([], {'domain': [['id', '=', self.dataset.ids]]}).done(function(records){
                    self.images_list = records
                    if (self.images_list.length == 0) {
                        self.do_warn(_t("Image"), _t("Image not available !"));
                        return false;
                    }
                    self.image_list_dialog = new instance.web.Dialog(self, {
                        title: _t("Image List"),
                        width: '840px',
                        height: '70%',
                        min_width: '600px',
                        min_height: '500px',
                        buttons: {
                            "Close": function() {
                                self.image_list_dialog.close();
                            }
                        },
                    }).open();
                    self.on_render_dialog();
                });
            });
        },

        on_render_dialog: function() {
            var self = this;
            var images_list = [];
            var images_list = self.images_list
            var model = self.dataset.model
            var url_list = [];
            var images = [];
            var start = 0;
            if (images_list) {
                _.each(images_list, function(img) {
                    var src=window.location.origin + "/web/binary/image?model=" + model + "&field=image&id="+img.id
                    if(img.image){
                        src="data:image/jpeg;base64,"+img.image
                    }
                    if (img) {
                        if (img['title']) {
                            url_list.push({
                                'name': img['title'],
                                'path': src,
                                'id':img.id
                            })
                        } else {
                            url_list.push({
                                'name': 'Image',
                                'path': src,
                                'id':img.id
                            })
                        }
                    }
                });
            } else {
                return false;
            }
            
            for (var i = 1; i <= Math.ceil(url_list.length / 4); i++) {
                images.push(url_list.slice(start, start + 4))
                start = i * 4;
            }
            self.image_list_dialog.$el.html(QWeb.render('DialogImageList', {
                'widget': self,
                'image_list': images,
                'readonly':$(".oe_form_buttons_edit")[0].style.display != 'none' ? true: false
            }));
            self.image_list_dialog.$el.find(".oe-remove-image").click(function() {
                self.do_remove_image(this, true);
            });
        },

        do_remove_image: function(curr_id, dialog) {
            var self = this;
            self.do_delete([ parseInt($(curr_id)[0].id)]);
            $(curr_id).closest('table.hoverbox').parent().remove();
        },

    });

}
openerp.web_widget_multi_image = function(instance) {
    instance.web_widget_multi_image = instance.web_widget_multi_image || {};
    openerp_web_widget_multi_image(instance);
}