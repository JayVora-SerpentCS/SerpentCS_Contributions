function openerp_web_widget_multi_image(instance){

    var QWeb = instance.web.qweb;
    var _t     = instance.web._t;

    instance.web.form.widgets.add('image_multi', 'instance.web.form.FieldBinaryImageMulti');

    instance.web.form.FieldBinaryImageMulti = instance.web.form.FieldBinaryImage.extend({
        template: 'FieldBinaryImageMulti',
        init: function(field_manager, node) {
            var self = this;
            this._super(field_manager, node);
            this.binary_value = false;
            this.useFileAPI = !window.FileReader;
            this.max_upload_size = 25 * 1024 * 1024; // 25Mo
            if (!this.useFileAPI) {
                this.fileupload_id = _.uniqueId('oe_fileupload');
                $(window).on(this.fileupload_id, function() {
                    var args = [].slice.call(arguments).slice(1);
                    self.on_file_uploaded.apply(self, args);
                });
            }
        },
        initialize_content: function() {
            this._super();
            var self = this;
            var dataset = new instance.web.DataSetSearch(this, 'res.users', {}, []);
            dataset.read_ids([instance.session.uid], ['name']).then(function(res) {
                if (res) self.user_name = res[0].name;
            });
            self.$el.find('.oe-image-preview').click(self.on_preview_button);
            self.$el.find('.oe_image_list').click(self.on_list_image);
        },
        on_file_uploaded_and_valid: function(size, name, content_type, orignal_file_name, date) {
            if (name) {
                var data_dict = {
                    "size": instance.web.human_size(size),
                    "name": name,
                    "content_type": content_type,
                    "date": date,
                    "orignal_name": orignal_file_name,
                    'user': this.user_name
                };
                var data = JSON.parse(this.get('value'));
                if (data) {
                    data.push(data_dict);
                } else {
                    data = [data_dict];
                }
                this.internal_set_value(JSON.stringify(data));
                this.binary_value = true;
                this.set_filename(name);
                this.render_value();
                this.do_warn(_t("File Upload"), _t("File Upload Successfully !"));
            } else {
                this.do_warn(_t("File Upload"), _t("There was a problem while uploading your file"));
            }
        },
        on_list_image: function() {
            var images_list = this.get('value');
            var self = this;
            if (!this.get('value')) {
                this.do_warn(_t("Image"), _t("Image not available !"));
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
            this.on_render_dialog();
        },
        on_render_dialog: function() {
            var self = this;
            var images_list = JSON.parse(this.get('value'));
            var url_list = [];
            var images = [];
            var start = 0;
            if (images_list) {
                _.each(images_list, function(img) {
                    if (img) {
                        if (img['img_title']) {
                            url_list.push({
                                'name': img['img_title'],
                                'path': img['name']
                            })
                        } else {
                            url_list.push({
                                'name': img['orignal_name'],
                                'path': img['name']
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
                'image_list': images
            }));
            self.image_list_dialog.$el.find(".oe-remove-image").click(function() {
                self.do_remove_image(this, true);
            });
        },
        render_value: function() {
            var self = this;
            var images_list = JSON.parse(this.get('value'));
            self.$el.find('#imagedescription').remove();
            var $img = QWeb.render("ImageDescription", {
                image_list: images_list,
                widget: self
            });
            self.$el.append($img);
            self.$el.find(".oe_image_row").click(function() {
                if (this.id) {
                    var clicked = this.id;
                    var name_desc = "";
                    _.each(images_list, function(img) {
                        if (img['name'] == clicked) {
                            var title = img['img_title'] ? img['img_title'] : ''
                            var description = img['description'] ? img['description'] : ''
                            name_desc = 'Title:-  ' + title + '<br/>Description:-  ' + description
                        }
                    });
                    self.do_display_image(this, name_desc);
                }
            });
            this.$el.find(".oe_list_record_delete").click(function() {
                if (this.id) {
                    self.do_remove_image(this, false);
                }
            });
            this.$el.find(".oe-record-edit-link").click(function() {
                var selected_rec = this;
                var img_data = JSON.parse(self.get('value'));
                _.each(img_data, function(img) {
                    if (img.name == selected_rec.id) {
                        self.name_display = img.img_title ? img.img_title : '';
                        self.description_display = img.description ? img.description : '';
                    }
                });
                self.edit_img_dialog = $(QWeb.render('edit_img_details', {
                    widget: self
                })).dialog({
                    resizable: false,
                    modal: true,
                    title: _t("Edit Image Details"),
                    width: 500,
                    buttons: {
                        "Ok": function() {
                            var new_list = [];
                            if (selected_rec.id && img_data) {
                                _.each(img_data, function(img) {
                                    if (img['name'] != selected_rec.id) {
                                        new_list.push(img)
                                    } else {
                                        img["img_title"] = self.edit_img_dialog.find('#img_title').val()
                                        img["description"] = self.edit_img_dialog.find('#description').val()
                                        new_list.push(img)
                                    }
                                });
                                self.internal_set_value(JSON.stringify(new_list));
                                self.invalid = false
                                self.dirty = true
                                self.render_value();
                                $(this).dialog("close");
                            }
                        },
                        "Close": function() {
                            $(this).dialog("close");
                        }
                    },
                });
            });
        },
        do_display_image: function(curr_id, name_desc) {
            this.$el.find('.oe-image-preview').lightbox({
                fitToScreen: true,
                jsonData: [{
                    "url": curr_id.id,
                    "title": name_desc
                }],
                loopImages: true,
                imageClickClose: false,
                disableNavbarLinks: true
            });
        },
        do_remove_image: function(curr_id, dialog) {
            var self = this;
            var images_list = JSON.parse(this.get('value'));
            if (images_list) {
                var new_list = [];
                if (confirm(_t("Are you sure to remove this image?"))) {
                    _.each(images_list, function(img) {
                        if (img['name'] != curr_id.id) {
                            new_list.push(img)
                        }else{
                            self.rpc("/web/binary/removeimage", {path: img['name']})
                        }
                    });
                    if(new_list.length > 0){
                        self.internal_set_value(JSON.stringify(new_list));
                    }else{
                        self.internal_set_value(0);
                    }
                    this.invalid = false
                    this.dirty = true
                    if (dialog) {
                        this.on_render_dialog();
                    } else {
                        this.render_value();
                    }
                }
            }
        },
        on_preview_button: function() {
            var images_list = JSON.parse(this.get('value'));
            var url_list = [];
            var self = this;
            if (images_list && !_.isEmpty(images_list)) {
                _.each(images_list, function(img) {
                    if (img) {
                        var title = img['img_title'] ? img['img_title'] : ''
                        var description = img['description'] ? img['description'] : ''
                        url_list.push({
                            "url": img['name'],
                            "title": 'Title:-' + title + '<br/>Description:-' + description
                        })
                    }
                });
            } else {
                this.do_warn("Image", "Image not available !");
                return false;
            }
            this.$el.find('.oe-image-preview').lightbox({
                fitToScreen: true,
                jsonData: url_list,
                loopImages: true,
                imageClickClose: false,
                disableNavbarLinks: true
            });
        },
    });
}
openerp.web_widget_multi_image = function(instance) {
    instance.web_widget_multi_image = instance.web_widget_multi_image || {};
    openerp_web_widget_multi_image(instance);
}