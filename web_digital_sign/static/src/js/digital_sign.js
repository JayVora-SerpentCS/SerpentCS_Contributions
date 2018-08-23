odoo.define('web_digital_sign.web_digital_sign', function(require) {
    "use strict";

    var core = require('web.core');
    var FormView = require('web.FormView');
    var utils = require('web.utils');
    var session = require('web.session');
    var Model = require('web.Model');

    var _t = core._t;
    var QWeb = core.qweb;

    var FieldSignature = core.form_widget_registry.map.image.extend({
        template: 'FieldSignature',
        placeholder: "/web/static/src/img/placeholder.png",
        initialize_content: function() {
            var self = this;
            this.$el.find('> img').remove();
            this.$el.find('.signature > canvas').remove();
            var sign_options = {'decor-color' : '#D1D0CE', 'color': '#000', 'background-color': '#fff','height':'150','width':'550'};
            this.$el.find(".signature").jSignature("init",sign_options);
            this.$el.find(".signature").attr({"tabindex": "0",'height':"100"});
            this.empty_sign = this.$el.find(".signature").jSignature("getData",'image');
            this.$el.find('#sign_clean').click(this.on_clear_sign);
            this.$el.find('.save_sign').click(this.on_save_sign);
        },
        on_clear_sign: function() {
            var self = this;
            this.$el.find(".signature > canvas").remove();
            this.$el.find('> img').remove();
            this.$el.find(".signature").attr("tabindex", "0");
            var sign_options = {'decor-color' : '#D1D0CE', 'color': '#000', 'background-color': '#fff','height':'150','width':'550','clear': true};
            this.$el.find(".signature").jSignature(sign_options);
            this.$el.find(".signature").focus();
            self.set('value', false);
        },
        on_save_sign: function(value_) {
            var self = this;
            this.$el.find('> img').remove();
            var signature = self.$el.find(".signature").jSignature("getData",'image');
            var is_empty = signature
                ? self.empty_sign[1] === signature[1]
                : false;
            if (! is_empty && typeof signature !== "undefined" && signature[1]) {
                self.set('value',signature[1]);
            }
        },
        render_value: function() {
            var self = this;
            var url = this.placeholder;
            if (this.get('value') && !utils.is_bin_size(this.get('value'))) {
                url = 'data:image/png;base64,' + this.get('value');
            } else if (this.get('value')) {
                url = this.session.url('/web/binary/image', {
                    model: this.view.dataset.model,
                    id: JSON.stringify(this.view.datarecord.id || null),
                    field:  this.options.preview_image
                    ? this.options.preview_image
                            : this.name,
                    t: new Date().getTime()
                });
            } else {
                url = this.placeholder;
            }
            if (this.view.get("actual_mode") === 'view' || this.get('effective_readonly')) {
                var $img = $(QWeb.render("FieldBinaryImage-extend", { widget: this, url: url }));
                this.$el.find('> img').remove();
                this.$el.find(".signature").hide();
                this.$el.prepend($img);
                $img.load(function() {
                    if (! self.options.size) {
                        return;
                    }
                    $img.css("max-width", "" + self.options.size[0] + "px");
                    $img.css("max-height", "" + self.options.size[1] + "px");
                    $img.css("margin-left", "" + (self.options.size[0] - $img.width()) / 2 + "px");
                    $img.css("margin-top", "" + (self.options.size[1] - $img.height()) / 2 + "px");
                });
                $img.on('error', function() {
                    $img.attr('src', self.placeholder);
                    self.do_warn(_t("Image"), _t("Could not display the selected image."));
                });
            } else if (this.view.get("actual_mode") === 'edit') {
                this.$el.find('> img').remove();
                if (this.get('value')) {
                    var field_name = this.options.preview_image
                        ? this.options.preview_image
                                : this.name;
                    new Model(this.view.dataset.model).call("read", [this.view.datarecord.id, [field_name]]).done(function(data) {
                        if (data) {
                            var field_desc = _.values(_.pick(data, field_name));
                            self.$el.find(".signature").jSignature("reset");
                            self.$el.find(".signature").jSignature("setData",'data:image/png;base64,'+field_desc[0]);
                        }
                    });
                } else {
                    this.$el.find('> img').remove();
                    this.$el.find('.signature > canvas').remove();
                    var sign_options = {'decor-color' : '#D1D0CE', 'color': '#000','background-color': '#fff','height':'150','width':'550'};
                    this.$el.find(".signature").jSignature("init",sign_options);
                }
                if(this.get('effective_readonly')){
                    var $img = $(QWeb.render("FieldBinaryImage-extend", { widget: this, url: url }));
                    this.$el.find('> img').remove();
                    this.$el.find(".signature").hide();
                    this.$el.prepend($img);
                    $img.load(function() {
                        if (! self.options.size) {
                            return;
                        }
                        $img.css("max-width", "" + self.options.size[0] + "px");
                        $img.css("max-height", "" + self.options.size[1] + "px");
                        $img.css("margin-left", "" + (self.options.size[0] - $img.width()) / 2 + "px");
                        $img.css("margin-top", "" + (self.options.size[1] - $img.height()) / 2 + "px");
                    });
                    $img.on('error', function() {
                        $img.attr('src', self.placeholder);
                        self.do_warn(_t("Image"), _t("Could not display the selected image."));
                    });
                }
          } else if (this.view.get("actual_mode") === 'create') {
              this.$el.find('> img').remove();
              this.$el.find('> canvas').remove();
              if (!this.get('value')) {
                  this.$el.find(".signature").empty().jSignature("init",{'decor-color' : '#D1D0CE', 'color': '#000','background-color': '#fff','height':'150','width':'550'});
              }
          }
        }
    });

    core.form_widget_registry.add('signature', FieldSignature);

    FormView.include({
        save: function() {
            this.$el.find('.save_sign').click();
            return this._super.apply(this, arguments);
        },
        _process_save: function(save_obj) {
            var self = this;
            var prepend_on_create = save_obj.prepend_on_create;
            var def_process_save = $.Deferred();
            try {
                var form_invalid = false,
                    values = {},
                    first_invalid_field = null,
                    readonly_values = {},
                    deferred = [];

                _.each(self.fields, function (f) {
                    var res = f.before_save();
                    if (res) {
                        deferred.push(res);
                        res.fail(function () {
                            form_invalid = true;
                            if (!first_invalid_field) {
                                first_invalid_field = f;
                            }
                        });
                    }
                });

                $.when.apply($, deferred).always(function () {

                    _.each(self.fields, function (f) {
                        if (!f.is_valid()) {
                            form_invalid = true;
                            if (!first_invalid_field) {
                                first_invalid_field = f;
                            }
                        } else if (f.name !== 'id' && (!self.datarecord.id || f._dirty_flag)) {
                            // Special case 'id' field, do not save this field
                            // on 'create' : save all non readonly fields
                            // on 'edit' : save non readonly modified fields
                            if (!f.get("readonly")) {
                                values[f.name] = f.get_value(true);
                            } else {
                                if(f.widget == 'signature'){
                                    values[f.name] = f.get_value(true);
                                }
                                else{
                                    readonly_values[f.name] = f.get_value(true);
                                }
                            }
                        }

                    });

                    // Heuristic to assign a proper sequence number for new records that
                    // are added in a dataset containing other lines with existing sequence numbers
                    if (!self.datarecord.id && self.fields.sequence &&
                        !_.has(values, 'sequence') && !_.isEmpty(self.dataset.cache)) {
                        // Find current max or min sequence (editable top/bottom)
                        var current = _[prepend_on_create ? "min" : "max"](
                            _.map(self.dataset.cache, function(o){return o.values.sequence})
                        );
                        values['sequence'] = prepend_on_create ? current - 1 : current + 1;
                    }
                    if (form_invalid) {
                        self.set({'display_invalid_fields': true});
                        first_invalid_field.focus();
                        self.on_invalid();
                        def_process_save.reject();
                    } else {
                        self.set({'display_invalid_fields': false});
                        var save_deferral;
                        if (!self.datarecord.id) {
                            // Creation save
                            save_deferral = self.dataset.create(values, {readonly_fields: readonly_values}).then(function(r) {
                                return self.record_created(r, prepend_on_create);
                            }, null);
                        } else if (_.isEmpty(values)) {
                            // Not dirty, noop save
                            save_deferral = $.Deferred().resolve({}).promise();
                        } else {
                            // Write save
                            save_deferral = self.dataset.write(self.datarecord.id, values, {readonly_fields: readonly_values}).then(function(r) {
                                return self.record_saved(r);
                            }, null);
                        }
                        save_deferral.then(function(result) {
                            def_process_save.resolve(result);
                        }).fail(function() {
                            def_process_save.reject();
                        });
                    }
                });
            } catch (e) {
                console.error(e);
                return def_process_save.reject();
            }
            return def_process_save;
        },

    });

});

