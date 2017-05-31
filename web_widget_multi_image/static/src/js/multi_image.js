/*global common*/
odoo.define('web.MultiImage', function(require) {
    "use strict";

    var core = require('web.core');
    var utils = require('web.utils');
    var Widget = require('web.Widget');
    var ViewManager = require('web.ViewManager');
    var ControlPanel = require('web.ControlPanel');
    var ListView = require('web.ListView');
    var dataset = require('web.data');
    var Dialog = require('web.Dialog');
    var list_widget_registry = core.list_widget_registry;

    var QWeb = core.qweb;
    var _t = core._t;

    var X2ManyViewManager = ViewManager.extend({
        init: function(parent, datasett, views, flags, x2many_views) {
            // By default, render buttons and pager in X2M fields, but no sidebar
            flags = _.extend({}, flags, {
                headless: false,
                search_view: false,
                action_buttons: true,
                pager: true,
                sidebar: false,
            });
            this.control_panel = new ControlPanel(parent, "X2ManyControlPanel");
            this.set_cp_bus(this.control_panel.get_bus());
            this._super(parent, datasett, views, flags);
            this.registry = core.view_registry.extend(x2many_views);
        },
        start: function() {
            this.control_panel.prependTo(this.$el);
            return this._super();
        },
        switch_mode: function(mode, unused) {
            if (mode !== 'form') {
                return this._super(mode, unused);
            }
            var self = this;
            var id = self.x2m.dataset.index
                ? self.x2m.dataset.ids[self.x2m.dataset.index]
                : null;
            var pop = new common.FormViewDialog(this, {
                res_model: self.x2m.field.relation,
                res_id: id,
                context: self.x2m.build_context(),

                title: _t("Open: ") + self.x2m.string,
                create_function: function(data, options) {
                    return self.x2m.data_create(data, options);
                },
                write_function: function(idd, data, options) {
                    return self.x2m.data_update(idd, data, options).done(function() {
                        self.x2m.reload_current_view();
                    });
                },
                alternative_form_view: typeof self.x2m.field.views
                    ? self.x2m.field.views.form
                    : "undefined",
                parent_view: self.x2m.view,
                child_name: self.x2m.name,
                read_function: function(ids, fields, options) {
                    return self.x2m.data_read(ids, fields, options);
                },
                form_view_options: {
                    'not_interactible_on_create': true
                },
                readonly: self.x2m.get("effective_readonly")
            }).open();
            pop.on("elements_selected", self, function() {
                self.x2m.reload_current_view();
            });
        },
    });

    var MultiImage = core.form_widget_registry.map.one2many.include({
        init: function() {
            this._super.apply(this, arguments);
        },
        start: function() {
            this._super.apply(this, arguments);
        },
        load_views: function() {
        	var self = this;
            var view_types = this.node.attrs.mode;
            view_types = !!view_types ? view_types.split(",") : [this.default_view];
            var views = [];
            _.each(view_types, function(view_type) {
                if (! _.include(["list", "tree", "graph", "kanban"], view_type)) {
                    throw new Error(_.str.sprintf(_t("View type '%s' is not supported in X2Many."), view_type));
                }
                var view = {
                    view_id: false,
                    view_type: view_type === "tree" ? "list" : view_type,
                    fields_view: self.field.views && self.field.views[view_type],
                    options: {},
                };
                if(view.view_type === "list") {
                   _.extend(view.options, {
                      action_buttons: false, // to avoid 'Save' and 'Discard' buttons to appear in X2M fields
                      addable: null,
                      selectable: self.multi_selection,
                      multi_image: (self.node.attrs.widget
                              ? self.node.attrs.widget === 'image_multi'
                              : false)
                              ? true
                          : false,
                      sortable: true,
                      import_enabled: false,
                      deletable: true
                  });
                  if (self.get("effective_readonly")) {
                      _.extend(view.options, {
                          deletable: null,
                          reorderable: false,
                          multi_image: (self.node.attrs.widget
                                  ? self.node.attrs.widget === 'image_multi'
                                  : false)
                                  ? true
                              : false,
                      });
                  }
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

            this.viewmanager = new X2ManyViewManager(this, this.dataset, views, this.view_options, this.x2many_views);
            this.viewmanager.x2m = self;
            var def = $.Deferred().done(function() {
                self.initial_is_loaded.resolve();
            });
            this.viewmanager.on("controller_inited", self, function(view_type, controller) {
                controller.x2m = self;
                if (view_type == "list") {
                    if (self.get("effective_readonly")) {
                        controller.on('edit:before', self, function (e) {
                            e.cancel = true;
                        });
                        _(controller.columns).find(function (column) {
                            if (!(column instanceof list_widget_registry.get('field.handle'))) {
                                return false;
                            }
                            column.modifiers.invisible = true;
                            return true;
                        });
                    }
                } else if (view_type == "graph") {
                    self.reload_current_view();
                }
                def.resolve();
            });
            this.viewmanager.on("switch_mode", self, function(n_mode) {
                $.when(self.commit_value()).done(function() {
                    if (n_mode === "list") {
                        utils.async_when().done(function() {
                            self.reload_current_view();
                        });
                    }
                });
            });
            utils.async_when().done(function () {
                self.$el.addClass('o_view_manager_content');
                self.alive(self.viewmanager.attachTo(self.$el));
            });
            return def;
        },
    });

    ListView.include({

        load_list: function(data) {
            var self = this;
            var result = this._super.apply(this, arguments);
            this.$el.find('.oe-image-preview').click(function() {
                var url_list = [];
                var model = self.dataset.model;
                self.images_list = [];
                self.image_dataset = new dataset.DataSetSearch(self, self.model, {}, []);
                if (_.every(self.dataset.ids, function(i) { return _.isString(i)})){
                    return alert("Please Save the record when you are adding an image for the first time !!")
                } else if (_.every(self.dataset.ids, function(i) { return _.isNumber(i)})){
                    self.image_dataset.read_slice([], {
                        'domain': [
                            ['id', 'in', self.dataset.ids]
                        ]
                    }).done(function(records) {
                        self.images_list = records;
                        var images_list = self.images_list;
                        if (images_list && !_.isEmpty(images_list)) {
                            _.each(images_list, function(img) {
                                if (img) {
                                    var src = window.location.origin + "/web/binary/image?model=" + model + "&field=image&id=" + img.id;
                                    if (img.image) {
                                        src = "data:image/jpeg;base64," + img.image;
                                    }
                                    var title = img.title
                                        ? img.title
                                        : '';
                                    var description = img.description
                                        ? img.description
                                        : '';
                                    url_list.push({
                                        "url": src,
                                        "title": 'Title:-' + title + '<br/>Description:-' + description
                                    });
                                }
                            });
                        } else {
                            self.do_warn("Image", "Image not available !");
                            return;
                        }
                        self.$el.find('.oe-image-preview').lightbox({
                            fitToScreen: true,
                            jsonData: url_list,
                            loopImages: true,
                            imageClickClose: false,
                            disableNavbarLinks: true
                        });
                    });
                } else {
                     return alert("Please Save the record when you are adding an image for the first time !!")
                }
            });

            this.$el.find('.oe_image_list').click(function() {
                var url_list = [];
                var model = self.dataset.model;
                self.images_list = [];
                self.image_dataset = new dataset.DataSetSearch(self, self.model, {}, []);
                if (_.every(self.dataset.ids, function(i) { return _.isString(i)})){
                    return alert("Please Save the record when you are adding an image for the first time !!")
                } else if (_.every(self.dataset.ids, function(i) { return _.isNumber(i)})){
                    self.image_dataset.read_slice([], {
                        'domain': [
                            ['id', 'in', self.dataset.ids]
                        ]
                    }).done(function(records) {
                        self.images_list = records;
                        if (self.images_list.length === 0) {
                            self.do_warn(_t("Image"), _t("Image not available !"));
                            return;
                        }
                        self.image_list_dialog = new Dialog(self, {
                            title: _t("Image List"),
                            width: '840px',
                            height: '70%',
                            min_width: '600px',
                            min_height: '500px',
                            buttons: [{
                                text: _t("Close"),
                                click: function() {
                                    self.image_list_dialog.close();
                                },
                                close: true
                            }],
                        }).open();
                        self.on_render_dialog();
                    });
                } else {
                     return alert("Please Save the record when you are adding an image for the first time !!")
                }
            });
            return result;
        },

        on_render_dialog: function() {
            var self = this;
            var images_list = [];
            images_list = self.images_list;
            var model = self.dataset.model;
            var url_list = [];
            var images = [];
            var start = 0;
            if (images_list) {
                _.each(images_list, function(img) {
                    var src = window.location.origin + "/web/binary/image?model=" + model + "&field=image&id=" + img.id;
                    if (img.image) {
                        src = "data:image/jpeg;base64," + img.image;
                    }
                    if (img) {
                        if (img.title) {
                            url_list.push({
                                'name': img.title,
                                'path': src,
                                'id': img.id
                            });
                        } else {
                            url_list.push({
                                'name': 'Image',
                                'path': src,
                                'id': img.id
                            });
                        }
                    }
                });
            } else {
                return false;
            }

            for (var i = 1; i <= Math.ceil(url_list.length / 4); i++) {
                images.push(url_list.slice(start, start + 4));
                start = i * 4;
            }
            self.image_list_dialog.$el.html(QWeb.render('DialogImageList', {
                'widget': self,
                'image_list': images,
                'readonly': self.x2m.get('effective_readonly'),
            }));
            self.image_list_dialog.$el.find(".oe-remove-image").click(function() {
                self.do_remove_image(this, true);
            });
        },

        do_remove_image: function(curr_id, dialog) {
            var self = this;
            self.do_delete([parseInt($(curr_id)[0].id, 10)]);
            $(curr_id).closest('table.hoverbox').parent().remove();
        },

    });
    return MultiImage;
});
