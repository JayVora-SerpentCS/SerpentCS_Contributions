openerp.web_groupby_expand = function (openerp) {
    var _t = openerp.web._t,
        _lt = openerp.web._lt;
    var QWeb = openerp.web.qweb;

    openerp.web.ListView.Groups.include({
        init:function (view, options) {
            this._super(view, options);
            this.groups_auto = [];
        },
        render: function (post_render) {
            var self = this;
            var $el = $('<tbody>');
            this.elements = [$el[0]];

            this.datagroup.list(
                _(this.view.visible_columns).chain()
                    .filter(function (column) { return column.tag === 'field' })
                    .pluck('name').value(),
                function (groups) {
                    self.view.$pager.find('.oe_pager_group').hide();
                    self.view.$pager.find('.oe_list_pager_state').text(self.view._limit ? self.view._limit : '∞');
                    $el[0].appendChild(
                        self.render_groups(groups));
                    if (post_render) { post_render(); }
                    if (self.options.expand){
                        self.render_auto_groups(self.groups_auto);
                    }
                }, function (dataset) {
                    self.render_dataset(dataset).done(function (list) {
                        self.children[null] = list;
                        self.elements =
                            [list.$current.replaceAll($el)[0]];
                        self.setup_resequence_rows(list, dataset);
                        if (post_render) { post_render(); }
                    });
                });
            return $el;
        },

        render_groups: function (datagroups) {
            var self = this;
            var placeholder = this.make_fragment();
            _(datagroups).each(function (group) {
                if (self.children[group.value]) {
                    self.records.proxy(group.value).reset();
                    delete self.children[group.value];
                }
                var child = self.children[group.value] = new (self.view.options.GroupsType)(self.view, {
                    records: self.records.proxy(group.value),
                    options: self.options,
                    columns: self.columns
                });
                self.bind_child_events(child);
                child.datagroup = group;

                var $row = child.$row = $('<tr class="oe_group_header">');
                self.groups_auto.push([$row,child])
                if (group.openable && group.length) {
                    $row.click(function (e) {
                        if (!$row.data('open')) {
                            $row.data('open', true)
                                .find('span.ui-icon')
                                    .removeClass('ui-icon-triangle-1-e')
                                    .addClass('ui-icon-triangle-1-s');
                            child.open(self.point_insertion(e.currentTarget));
                        } else {
                            $row.removeData('open')
                                .find('span.ui-icon')
                                    .removeClass('ui-icon-triangle-1-s')
                                    .addClass('ui-icon-triangle-1-e');
                            child.close();
                            // force recompute the selection as closing group reset properties
                            var selection = self.get_selection();
                            $(self).trigger('selected', [selection.ids, this.records]);
                        }
                    });
                }
                placeholder.appendChild($row[0]);

                var $group_column = $('<th class="oe_list_group_name">').appendTo($row);
                // Don't fill this if group_by_no_leaf but no group_by
                if (group.grouped_on) {
                    var row_data = {};
                    row_data[group.grouped_on] = group;
                    var group_label = _t("Undefined");
                    var group_column = _(self.columns).detect(function (column) {
                        return column.id === group.grouped_on; });
                    if (group_column) {
                        try {
                            group_label = group_column.format(row_data, {
                                value_if_empty: _t("Undefined"),
                                process_modifiers: false
                            });
                        } catch (e) {
                            group_label = _.str.escapeHTML(row_data[group_column.id].value);
                        }
                    } else {
                        group_label = group.value;
                        if (group_label instanceof Array) {
                            group_label = group_label[1];
                        }
                        if (group_label === false) {
                            group_label = _t('Undefined');
                        }
                        group_label = _.str.escapeHTML(group_label);
                    }
                        
                    // group_label is html-clean (through format or explicit
                    // escaping if format failed), can inject straight into HTML
                    $group_column.html(_.str.sprintf(_t("%s (%d)"),
                        group_label, group.length));
                    if (group.length && group.openable) {
                        // Make openable if not terminal group & group_by_no_leaf
                        $group_column.prepend('<span class="ui-icon ui-icon-triangle-1-e" style="float: left;">');
                        self.view.$buttons.find('.oe-list-expand').removeAttr("disabled")
                    } else {
                        // Kinda-ugly hack: jquery-ui has no "empty" icon, so set
                        // wonky background position to ensure nothing is displayed
                        // there but the rest of the behavior is ui-icon's
                        $group_column.prepend('<span class="ui-icon" style="float: left; background-position: 150px 150px">');
                    }
                }
                self.indent($group_column, group.level);

                if (self.options.selectable) {
                    $row.append('<td>');
                }
                _(self.columns).chain()
                    .filter(function (column) { return column.invisible !== '1'; })
                    .each(function (column) {
                        if (column.meta) {
                            // do not do anything
                        } else if (column.id in group.aggregates) {
                            var r = {};
                            r[column.id] = {value: group.aggregates[column.id]};
                            $('<td class="oe_number">')
                                .html(column.format(r, {process_modifiers: false}))
                                .appendTo($row);
                        } else {
                            $row.append('<td>');
                        }
                    });
                if (self.options.deletable) {
                    $row.append('<td class="oe_list_group_pagination">');
                }
            });
            return placeholder;
        },

        render_auto_groups: function (groups_auto) {
            var self = this;
            if (!groups_auto) {
                groups_auto = self.groups_auto;
            }
            _.each(groups_auto, function(vals){
                if(vals[1].datagroup.openable){
                    if (!vals[0].data('open')) {
                        vals[0].data('open', true)
                            .find('span.ui-icon')
                                .removeClass('ui-icon-triangle-1-e')
                                .addClass('ui-icon-triangle-1-s');
                        vals[1].open(self.point_insertion(vals[0]));
                    } else {
                        vals[0].removeData('open')
                            .find('span.ui-icon')
                                .removeClass('ui-icon-triangle-1-s')
                                .addClass('ui-icon-triangle-1-e');
                        vals[1].close();
                    }
                }
            })
        },
    });
    
    openerp.web.ListView.include({
        set_default_options: function (options) {
            this._super(options);
            _.defaults(this.options, {
                expand : false,
//                GroupsType: openerp.web.ListView.Groups,
//                ListType: openerp.web.ListView.List
            });
        },
        load_list: function(data) {
            var self = this;
            this.fields_view = data;
            this.name = "" + this.fields_view.arch.attrs.string;

            if (this.fields_view.arch.attrs.colors) {
                this.colors = _(this.fields_view.arch.attrs.colors.split(';')).chain()
                    .compact()
                    .map(function(color_pair) {
                        var pair = color_pair.split(':'),
                            color = pair[0],
                            expr = pair[1];
                        return [color, py.parse(py.tokenize(expr)), expr];
                    }).value();
            }

            if (this.fields_view.arch.attrs.fonts) {
                this.fonts = _(this.fields_view.arch.attrs.fonts.split(';')).chain().compact()
                    .map(function(font_pair) {
                        var pair = font_pair.split(':'),
                            font = pair[0],
                            expr = pair[1];
                        return [font, py.parse(py.tokenize(expr)), expr];
                    }).value();
            }

            this.setup_columns(this.fields_view.fields, this.grouped);

            this.$el.html(QWeb.render(this._template, this));
            this.$el.addClass(this.fields_view.arch.attrs['class']);

            // Head hook
            // Selecting records
            this.$el.find('.oe_list_record_selector').click(function(){
                self.$el.find('.oe_list_record_selector input').prop('checked',
                    self.$el.find('.oe_list_record_selector').prop('checked')  || false);
                var selection = self.groups.get_selection();
                $(self.groups).trigger(
                    'selected', [selection.ids, selection.records]);
            });

            // Add button
            if (!this.$buttons) {
                this.$buttons = $(QWeb.render("ListView.buttons", {'widget':self}));
                if (this.options.$buttons) {
                    this.$buttons.appendTo(this.options.$buttons);
                } else {
                    this.$el.find('.oe_list_buttons').replaceWith(this.$buttons);
                }
                this.$buttons.find('.oe-list-expand').click(function(){
                    self.options.expand = true;
                    self.groups.render_auto_groups(false)
                })
                this.$buttons.find('.oe_list_add')
                        .click(this.proxy('do_add_record'))
                        .prop('disabled', this.grouped);
            }
            if(self.groups.datagroup.dataset){
                this.$buttons.find('.oe-list-expand').hide()
            }
            if(self.groups.datagroup.group_by == ""){
                this.$buttons.find('.oe-list-expand').attr("disabled","disabled");
            }else{
                this.$buttons.find('.oe-list-expand').removeAttr("disabled");
            }
            // Pager
            if (!this.$pager) {
                this.$pager = $(QWeb.render("ListView.pager", {'widget':self}));
                if (this.options.$buttons) {
                    this.$pager.appendTo(this.options.$pager);
                } else {
                    this.$el.find('.oe_list_pager').replaceWith(this.$pager);
                }

                this.$pager
                    .on('click', 'a[data-pager-action]', function () {
                        var $this = $(this);
                        var max_page = Math.floor(self.dataset.size() / self.limit());
                        switch ($this.data('pager-action')) {
                            case 'first':
                                self.page = 0; break;
                            case 'last':
                                self.page = max_page - 1;
                                break;
                            case 'next':
                                self.page += 1; break;
                            case 'previous':
                                self.page -= 1; break;
                        }
                        if (self.page < 0) {
                            self.page = max_page;
                        } else if (self.page > max_page) {
                            self.page = 0;
                        }
                        self.reload_content();
                    }).find('.oe_list_pager_state')
                        .click(function (e) {
                            e.stopPropagation();
                            var $this = $(this);

                            var $select = $('<select>')
                                .appendTo($this.empty())
                                .click(function (e) {e.stopPropagation();})
                                .append('<option value="80">80</option>' +
                                        '<option value="200">200</option>' +
                                        '<option value="500">500</option>' +
                                        '<option value="2000">2000</option>' +
                                        '<option value="NaN">' + _t("Unlimited") + '</option>')
                                .change(function () {
                                    var val = parseInt($select.val(), 10);
                                    self._limit = (isNaN(val) ? null : val);
                                    self.page = 0;
                                    self.reload_content();
                                }).blur(function() {
                                    $(this).trigger('change');
                                })
                                .val(self._limit || 'NaN');
                        });
            }

            // Sidebar
            if (!this.sidebar && this.options.$sidebar) {
                this.sidebar = new openerp.web.Sidebar(this);
                this.sidebar.appendTo(this.options.$sidebar);
                this.sidebar.add_items('other', _.compact([
                    { label: _t("Export"), callback: this.on_sidebar_export },
                    self.is_action_enabled('delete') && { label: _t('Delete'), callback: this.do_delete_selected }
                ]));
                this.sidebar.add_toolbar(this.fields_view.toolbar);
                this.sidebar.$el.hide();
            }
            //Sort
            if(this.dataset._sort.length){
                if(this.dataset._sort[0].indexOf('-') == -1){
                    this.$el.find('th[data-id=' + this.dataset._sort[0] + ']').addClass("sortdown");
                }else {
                    this.$el.find('th[data-id=' + this.dataset._sort[0].split('-')[1] + ']').addClass("sortup");
                }
            }
            this.trigger('list_view_loaded', data, this.grouped);
        },

        do_search: function (domain, context, group_by) {
            this._super(domain, context, group_by);
            this.options.expand = false;
            this.groups.groups_auto = []
        },
    });
};
