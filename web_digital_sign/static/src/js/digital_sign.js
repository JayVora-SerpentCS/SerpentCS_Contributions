openerp.web_digital_sign = function(instance) {
    var _t = instance.web._t;
    var QWeb = instance.web.qweb;
    var images = {}
    instance.web.form.widgets.add('signature', 'instance.web.form.FieldSignature');

    instance.web.form.FieldSignature = instance.web.form.FieldBinaryImage.extend({
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
            if (this.get('value') && !instance.web.form.is_bin_size(this.get('value'))) {
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
            var $img = $(QWeb.render("FieldBinaryImage-img", { widget: this, url: url }));
            this.$el.find('img').remove();
            if(this.view.get("actual_mode") !== 'edit' && this.view.get("actual_mode") !== 'create'){
            	this.$el.find('.signature > canvas').remove();
            	this.$el.prepend($img);
            }
            else if (this.view.get("actual_mode") === 'edit') {
                this.$el.find('> img').remove();
                if (this.get('value')) {
                    var field_name = this.options.preview_image
                        ? this.options.preview_image
                                : this.name;
                    new instance.web.Model(this.view.dataset.model).call("read", [this.view.datarecord.id, [field_name]]).done(function(data) {
                        if (data) {
//                            self.$el.find(".signature").jSignature("reset");
                            self.$el.find(".signature").jSignature("setData",'data:image/png;base64,'+data[field_name]);
                        }
                    });
                } else {
                    this.$el.find('> img').remove();
                    this.$el.find('.signature > canvas').remove();
                    var sign_options = {'decor-color' : '#D1D0CE', 'color': '#000','background-color': '#fff','height':'150','width':'550'};
                    this.$el.find(".signature").jSignature("init",sign_options);
                }
          } else if (this.view.get("actual_mode") === 'create') {
              this.$el.find('> img').remove();
              this.$el.find('> canvas').remove();
              if (!this.get('value')) {
                  this.$el.find(".signature").empty().jSignature("init",{'decor-color' : '#D1D0CE', 'color': '#000','background-color': '#fff','height':'150','width':'550'});
              }
              else if(this.get('value')){
                  this.$el.prepend($img);
              }
          }
        }
    });
    
    instance.web.FormView.include({
        save: function(prepend_on_create) {
            var self = this;
            $('.save_sign').click()
            return this._super.apply(this, arguments);
        },
    })
};
