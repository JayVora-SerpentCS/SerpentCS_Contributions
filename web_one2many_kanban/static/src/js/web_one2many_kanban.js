/*global session*/
odoo.define('web_one2many_kanban.web_one2many_kanban', function(require) {
    "use strict";

    var core = require('web.core');
    var Model = require('web.DataModel');
    var data = require('web.data');
    var utils = require('web.utils');
    var data_manager = require('web.data_manager');
    var KanbanRecord = require('web_kanban.Record');
    var KanbanView = require('web_kanban.KanbanView');
    var kanban_widgets = require('web_kanban.widgets');
    var KanbanColumn = require('web_kanban.Column');
    var fields_registry = kanban_widgets.registry;
    var QWeb = core.qweb;
    var config = require('web.config');
    var pyeval = require('web.pyeval');
    var _t = core._t;

    /*Kanban view For one2many*/
    function qweb_add_if(node, conditions) {
        var condition = conditions;
        if (node.attrs[QWeb.prefix + '-if']) {
            condition = _.str.sprintf("(%s) and (%s)", node.attrs[QWeb.prefix + '-if'], condition);
        }
        node.attrs[QWeb.prefix + '-if'] = condition;
    }

    function transform_qweb_template(node, fvg, many2manys, current) {
        var self = current;
        // Process modifiers
        if (node.tag && node.attrs.modifiers) {
            var modifiers = JSON.parse(node.attrs.modifiers || '{}');
            if (modifiers.invisible) {
                qweb_add_if(node, _.str.sprintf("!kanban_compute_domain(%s)", JSON.stringify(modifiers.invisible)));
            }
        }
        switch (node.tag) {
            case 'div':
            case 'tr':
            case 'table':
            case 'td':
            case 'span':
            case 't':
                self.dataset.o2m_field = {};
                if (typeof node.attrs['t-foreach'] !== "undefined") {
                    var field_name = node.attrs['t-foreach'].split('.')[1];
                    if (typeof field_name !== "undefined") {
                        self.field_details = self.fields_view.fields[field_name];
                        if (self.field_details.type === 'one2many' && (typeof self.field_details.related !== "undefined" || typeof self.field_details.relation_field !== "undefined") && self.same_field.indexOf(field_name) === -1) {
                            self.same_field.push(field_name);
                            var model = self.field_details.relation;
                            self.o2m_dataset = new data.DataSetSearch(self, model, {}, []);
                            self.o2m_dataset.call('fields_get').done(function(o2mdata) {
                                var fields = [];
                                _.each(o2mdata, function(field_def, field_nm) {
                                    if (field_def.type !== 'many2many') {
                                        fields.push(field_nm);
                                    }
                                });
                                self.dataset.o2m_field[field_name] = {
                                    'field_name': field_name,
                                    'model': model,
                                    'fields': fields
                                };
                            });
                        }
                    }
                }
                break;
            case 'field':
                var ftype = fvg.fields[node.attrs.name].type;
                ftype = node.attrs.widget
                    ? node.attrs.widget
                    : ftype;
                if (ftype === 'many2many') {
                    if (_.indexOf(many2manys, node.attrs.name) < 0) {
                        many2manys.push(node.attrs.name);
                    }
                    node.tag = 'div';
                    node.attrs.class = (node.attrs.class || '') + ' oe_form_field o_form_field_many2manytags o_kanban_tags';
                } else if (fields_registry.contains(ftype)) {
                    // do nothing, the kanban record will handle it
                } else {
                    node.tag = QWeb.prefix;
                    node.attrs[QWeb.prefix + '-esc'] = 'record.' + node.attrs.name + '.value';
                }
                break;
            case 'button':
            case 'a':
                var type = node.attrs.type || '';
                if (_.indexOf('action,object,edit,open,delete,url,set_cover'.split(','), type) !== -1) {
                    _.each(node.attrs, function(v, k) {
                        if (_.indexOf('icon,type,name,args,string,context,states,kanban_states'.split(','), k) !== -1) {
                            node.attrs['data-' + k] = v;
                            delete node.attrs[k];
                        }
                    });
                    if (node.attrs['data-string']) {
                        node.attrs.title = node.attrs['data-string'];
                    }
                    if (node.attrs['data-icon']) {
                        node.children = [{
                            tag: 'img',
                            attrs: {
                                src: session.prefix + '/web/static/src/img/icons/' + node.attrs['data-icon'] + '.png',
                                width: '16',
                                height: '16'
                            }
                        }];
                    }
                    if (node.tag === 'a' && node.attrs['data-type'] !== "url") {
                        node.attrs.href = '#';
                    } else {
                        node.attrs.type = 'button';
                    }
                    node.attrs.class = (node.attrs.class || '') + ' oe_kanban_action oe_kanban_action_' + node.tag;
                }
                break;
        }
        if (node.children) {
            for (var i = 0, ii = node.children.length; i < ii; i++) {
                transform_qweb_template(node.children[i], fvg, many2manys, self);
            }
        }
    }


    KanbanView.include({

        willStart: function() {
            // add qweb templates
            this.same_field = [];
            for (var i = 0, ii = this.fields_view.arch.children.length; i < ii; i++) {
                var child = this.fields_view.arch.children[i];
                if (child.tag === "templates") {
                    transform_qweb_template(child, this.fields_view, this.many2manys, this);
                    // transform_qweb_template(), among other things, identifies and processes the
                    // many2manys. Unfortunately, it modifies the fields_view in place and, as
                    // the fields_view is stored in the JS cache, the many2manys are only identified the
                    // first time the fields_view is processed. We thus store the identified many2manys
                    // on the fields_view, so that we can retrieve them later. A better fix would be to
                    // stop modifying shared resources in place.
                    this.fields_view.many2manys = this.many2manys;
                    this.qweb.add_template(utils.json_node_to_xml(child));
                    break;
                } else if (child.tag === 'field') {
                    var ftype = child.attrs.widget || this.fields_view.fields[child.attrs.name].type;
                    if (ftype === "many2many" && "context" in child.attrs) {
                        this.m2m_context[child.attrs.name] = child.attrs.context;
                    }
                }
            }
            return this._super();
        },

        load_groups: function(option) {
            var self = this;
            var options = option;
            var group_by_field = options.group_by_field || options.default_group_by;
            this.fields_keys = _.uniq(this.fields_keys.concat(group_by_field));

            var fields_def = '';
            if (typeof this.fields_view.fields[group_by_field] === "undefined") {
                fields_def = data_manager.load_fields(this.dataset).then(function(fields) {
                    self.fields = fields;
                });
            }
            var load_groups_def = new Model(this.model, this.search_context, this.search_domain).query(this.fields_keys).group_by([group_by_field]).then(function(groups) {
                // Check in the arch the fields to fetch on the stage to get tooltips data.
                // Fetching data is done in batch for all stages, to avoid doing multiple
                // calls. The first naive implementation of group_by_tooltip made a call
                // for each displayed stage and was quite limited.
                // Data for the group tooltip (group_by_tooltip) and to display stage-related
                // legends for kanban state management (states_legend) are fetched in
                // one call.
                var group_by_fields_to_read = [];
                var group_options = {};
                var recurse = function(node) {
                    if (node.tag === "field" && node.attrs && node.attrs.options && node.attrs.name === group_by_field) {
                        options = pyeval.py_eval(node.attrs.options);
                        group_options = options;
                        var states_fields_to_read = _.map(
                            (options && options.states_legend) || {},
                            function(value, key, list) {
                                return value;
                            });
                        var tooltip_fields_to_read = _.map(
                            (options && options.group_by_tooltip) || {},
                            function(value, key, list) {
                                return key;
                            });
                        group_by_fields_to_read = _.union(
                            group_by_fields_to_read,
                            states_fields_to_read,
                            tooltip_fields_to_read);
                        return;
                    }
                    _.each(node.children, function(child) {
                        recurse(child);
                    });
                };
                recurse(self.fields_view.arch);

                // fetch group data (display information)
                var group_ids = _.without(typeof _.map(groups, function(elem) {
                    return elem.attributes.value[0];
                }), "undefined");
                if (self.grouped_by_m2o && group_ids.length) {
                    return new data.DataSet(self, self.relation).read_ids(group_ids, _.union(['display_name'], group_by_fields_to_read)).then(function(results) {
                        _.each(groups, function(group) {
                            var group_id = group.attributes.value[0];
                            var result = _.find(results, function(gdata) {
                                return group_id === gdata.id;
                            });
                            group.title = result
                                ? result.display_name
                                : _t("Undefined");
                            group.values = result;
                            group.id = group_id;
                            group.options = group_options;
                        });
                        return groups;
                    });
                } else {
                    _.each(groups, function(group) {
                        var value = group.attributes.value;
                        group.id = value instanceof Array
                            ? value[0]
                            : value;
                        var field = self.fields_view.fields[self.group_by_field];
                        if (field && field.type === "selection") {
                            value = _.find(field.selection, function(s) {
                                return s[0] === group.id;
                            });
                        }
                        group.title = (value instanceof Array
                            ? value[1]
                            : value) || _t("Undefined");
                        group.values = {};
                    });
                    return $.when(groups);
                }
            }).then(function(groups) {
                var undef_index = _.findIndex(groups, function(g) {
                    return g.title === _t("Undefined");
                });
                if (undef_index >= 1) {
                    var undef_group = groups[undef_index];
                    groups.splice(undef_index, 1);
                    groups.unshift(undef_group);
                }
                return groups;
            }).then(function(groups) {
                // load records for each group
                var is_empty = true;
                return $.when.apply(null, _.map(groups, function(group) {
                    var def = $.when([]);
                    var dataset = new data.DataSetSearch(self, self.dataset.model,
                        new data.CompoundContext(self.dataset.get_context(), group.model.context()), group.model.domain());
                    if (self.dataset._sort) {
                        dataset.set_sort(self.dataset._sort);
                    }
                    if (group.attributes.length >= 1) {
                        def = dataset.read_slice(self.fields_keys.concat(['__last_update']), {
                            'limit': self.limit
                        });
                    }
                    return def.then(function(records) {
                        self.dataset.ids.push.apply(self.dataset.ids, _.difference(dataset.ids, self.dataset.ids));
                        group.records = records;

                        dataset.o2m_field = self.dataset.o2m_field;

                        group.dataset = dataset;
                        is_empty = is_empty && !records.length;
                        return group;
                    });
                })).then(function() {
                    return {
                        groups: Array.prototype.slice.call(arguments, 0),
                        is_empty: is_empty,
                        grouped: true,
                    };
                });
            });
            return $.when(load_groups_def, fields_def);
        },

        render: function() {
            // cleanup
            this.$el.css({
                display: '-webkit-flex'
            });
            this.$el.css({
                display: 'flex'
            });
            this.$el.removeClass('o_kanban_ungrouped o_kanban_grouped o_kanban_nocontent');
            _.invoke(this.widgets, 'destroy');
            this.$el.empty();
            this.widgets = [];
            if (this.column_quick_create) {
                this.column_quick_create.destroy();
                this.column_quick_create = undefined;
            }

            this.record_options = {
                editable: this.is_action_enabled('edit'),
                deletable: this.is_action_enabled('delete'),
                fields: this.fields_view.fields,
                qweb: this.qweb,
                model: this.model,
                read_only_mode: this.options.read_only_mode,
            };

            // actual rendering
            var fragment = document.createDocumentFragment();
            if (this.data.grouped) {
                this.$el.addClass('o_kanban_grouped');
                this.render_grouped(fragment);
            } else {
                this.$el.addClass('o_kanban_ungrouped');
                this.render_ungrouped(fragment, this.$el);
            }
            if (this.data.is_empty && this.widgets.length === 0 && (!this.data.grouped || !this.is_action_enabled('group_create') || !this.grouped_by_m2o)) {
                this.$el.css("display", "block");
                this.$el.addClass("o_kanban_nocontent");
                this.render_no_content(fragment);
            }
            this.$el.append(fragment);
        },

        render_ungrouped: function(fragment, el) {
            var self = this;
            var options = _.clone(this.record_options);
            // add empty invisible divs to make sure that all kanban records are left aligned

            if (_.keys(self.dataset.o2m_field).length) {
                _.each(this.data.records, function(record) {
                    if (_.keys(self.dataset.o2m_field).length) {
                        _.each(self.dataset.o2m_field, function(ddata, index) {
                            var ids = record[ddata.field_name];
                            var model = ddata.model;
                            var fields = ddata.fields;
                            var o2m_model = new Model(model);
                            o2m_model.query(fields).filter([
                                ['id', 'in', ids]
                            ]).all().then(function(field_record) {
                                record[ddata.field_name] = field_record;
                                var kanban_record = new KanbanRecord(self, record, options);
                                self.widgets.push(kanban_record);
                                kanban_record.appendTo(fragment);
                                el.append(fragment);
                            });
                        });
                    }
                });

                for (var i = 0, ghost_div; i < 6; i++) {
                    ghost_div = $("<div>").addClass("o_kanban_record o_kanban_ghost o_kanban_flx");
                    ghost_div.appendTo(fragment);
                }
                this.postprocess_m2m_tags();

            } else {
                _.each(this.data.records, function(record) {
                    var kanban_record = new KanbanRecord(self, record, options);
                    self.widgets.push(kanban_record);
                    kanban_record.appendTo(fragment);
                });
            }
            // add empty invisible divs to make sure that all kanban records are left aligned
            for (var ii = 0, gst_div; ii < 6; ii++) {
                gst_div = $("<div>").addClass("o_kanban_record o_kanban_ghost");
                gst_div.appendTo(fragment);

            }
            this.postprocess_m2m_tags();
        },

        reload_record: function(record) {
            var self = this;
            this.dataset.read_ids([record.id], this.fields_keys.concat(['__last_update'])).done(function(records) {
                if (_.keys(self.dataset.o2m_field).length) {
                    var count = 0;
                    _.each(self.dataset.o2m_field, function(field, index) {
                        var ids = records[0][field.field_name];
                        var fields = field.fields;
                        var model = field.model;
                        var o2m_dataset = new data.DataSetSearch(self, model, {}, []);
                        o2m_dataset.read_slice(fields, {
                            'domain': [
                                ['id', 'in', ids]
                            ]
                        }).then(function(field_record) {
                            count++;
                            records[0][field.field_name] = field_record;
                            if (count === _.keys(self.dataset.o2m_field).length) {
                                if (records.length) {
                                    record.update(records[0]);
                                    self.postprocess_m2m_tags(record);
                                } else {
                                    record.destroy();
                                }
                            }
                        });
                    });
                } else {
                    if (records.length) {
                        record.update(records[0]);
                        self.postprocess_m2m_tags(record);
                    } else {
                        record.destroy();
                    }
                }
            });
        },

    });


    KanbanColumn.include({

        start: function() {
            var self = this;
            this.$header = this.$('.o_kanban_header');
            if (_.keys(self.dataset.o2m_field).length) {
                _.each(self.data_records, function(record) {
                    if (_.keys(self.dataset.o2m_field).length) {
                        var count = 0;
                        _.each(self.dataset.o2m_field, function(datas, index) {
                            var ids = record[datas.field_name];
                            var model = datas.model;
                            var fields = datas.fields;
                            var o2m_model = new Model(model);
                            o2m_model.query(fields).filter(
                                [
                                    ['id', 'in', ids]
                                ]).all().then(function(field_record) {
                                record[datas.field_name] = field_record;
                                count++;
                                self.add_record(record, {
                                    no_update: true
                                });
                            });
                        });
                    }
                });
            } else {
                for (var i = 0; i < this.data_records.length; i++) {
                    this.add_record(this.data_records[i], {
                        no_update: true
                    });
                }
            }
            this.$header.tooltip();
            if (config.device.size_class > config.device.SIZES.XS && this.draggable !== false) {
                // deactivate sortable in mobile mode.  It does not work anyway,
                // and it breaks horizontal scrolling in kanban views.  Someday, we
                // should find a way to use the touch events to make sortable work.
                this.$el.sortable({
                    connectWith: '.o_kanban_group',
                    revert: 0,
                    delay: 0,
                    items: '> .o_kanban_record:not(.o_updating)',
                    helper: 'clone',
                    cursor: 'move',
                    over: function() {
                        self.$el.addClass('o_kanban_hover');
                        self.update_column();
                    },
                    out: function() {
                        self.$el.removeClass('o_kanban_hover');
                    },
                    update: function(event, ui) {
                        var record = ui.item.data('record');
                        var index = self.records.indexOf(record);
                        var test2 = $.contains(self.$el[0], record.$el[0]);
                        record.$el.removeAttr('style'); // jqueryui sortable add display:block inline
                        if (index >= 0 && test2) {
                            // resequencing records
                            self.trigger_up('kanban_column_resequence');
                        } else if (index >= 0 && !test2) {
                            // removing record from this column
                            self.records.splice(self.records.indexOf(record), 1);
                            self.dataset.remove_ids([record.id]);
                        } else {
                            // adding record to this column
                            self.records.push(record);
                            record.setParent(self);
                            self.trigger_up('kanban_column_add_record', {
                                record: record
                            });
                        }
                        self.update_column();
                    }
                });
            }
            this.update_column();
            this.$el.click(function(event) {
                if (self.$el.hasClass('o_column_folded')) {
                    event.preventDefault();
                    self.folded = false;
                    self.update_column();
                }
            });
        },

    });

});
