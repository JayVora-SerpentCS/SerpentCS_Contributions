openerp.web_one2many_kanban = function(instance) {
    var QWeb = instance.web.qweb;
    var _t = instance.web._t;

    /*Kanban view For one2many*/

    instance.web_kanban.KanbanView.include({
        
        add_qweb_template: function() {
            this.same_field = []
            for (var i=0, ii=this.fields_view.arch.children.length; i < ii; i++) {
                var child = this.fields_view.arch.children[i];
                if (child.tag === "templates") {
                    this.transform_qweb_template(child);
                    this.qweb.add_template(instance.web.json_node_to_xml(child));
                    break;
                } else if (child.tag === 'field') {
                    this.extract_aggregates(child);
                }
            }
        },
        
        transform_qweb_template: function(node) {
            var qweb_add_if = function(node, condition) {
                if (node.attrs[QWeb.prefix + '-if']) {
                    condition = _.str.sprintf("(%s) and (%s)", node.attrs[QWeb.prefix + '-if'], condition);
                }
                node.attrs[QWeb.prefix + '-if'] = condition;
            };
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
                    var self =this
                    self.dataset.o2m_field = {}
                    if(node.attrs['t-foreach'] != undefined){
                        var field_name = node.attrs['t-foreach'].split('.')[1]
                        if(field_name != undefined){
                            self.field_details = this.fields_view.fields[field_name];
                            if(self.field_details.type == 'one2many' && (self.field_details.related != undefined || self.field_details.relation_field != undefined) && self.same_field.indexOf(field_name) == -1){
                                self.same_field.push(field_name)
                                var model = self.field_details.relation
                                self.o2m_dataset = new instance.web.DataSetSearch(self,model, {}, []);
                                self.o2m_dataset.call('fields_get').done(function(data) {
                                    var fields=[]
                                    _.each(data, function(field_def, field_name) {
                                        if(field_def.type != 'many2many'){
                                            fields.push(field_name)
                                        }
                                    });
                                    self.dataset.o2m_field[field_name] = {'field_name':field_name,'model':model,'fields':fields}
                                })
                            }
                        }
                    }
                    break;
                case 'field':
                    var ftype = this.fields_view.fields[node.attrs.name].type;
                    ftype = node.attrs.widget ? node.attrs.widget : ftype;
                    if (ftype === 'many2many') {
                        if (_.indexOf(this.many2manys, node.attrs.name) < 0) {
                            this.many2manys.push(node.attrs.name);
                        }
                        node.tag = 'div';
                        node.attrs['class'] = (node.attrs['class'] || '') + ' oe_form_field oe_tags';
                    } else if (instance.web_kanban.fields_registry.contains(ftype)) {
                        // do nothing, the kanban record will handle it
                    } else {
                        node.tag = QWeb.prefix;
                        node.attrs[QWeb.prefix + '-esc'] = 'record.' + node.attrs['name'] + '.value';
                    }
                    break;
                case 'button':
                case 'a':
                    var type = node.attrs.type || '';
                    if (_.indexOf('action,object,edit,open,delete'.split(','), type) !== -1) {
                        _.each(node.attrs, function(v, k) {
                            if (_.indexOf('icon,type,name,args,string,context,states,kanban_states'.split(','), k) != -1) {
                                node.attrs['data-' + k] = v;
                                delete(node.attrs[k]);
                            }
                        });
                        if (node.attrs['data-string']) {
                            node.attrs.title = node.attrs['data-string'];
                        }
                        if (node.attrs['data-icon']) {
                            node.children = [{
                                tag: 'img',
                                attrs: {
                                    src: instance.session.prefix + '/web/static/src/img/icons/' + node.attrs['data-icon'] + '.png',
                                    width: '16',
                                    height: '16'
                                }
                            }];
                        }
                        if (node.tag == 'a') {
                            node.attrs.href = '#';
                        } else {
                            node.attrs.type = 'button';
                        }
                        node.attrs['class'] = (node.attrs['class'] || '') + ' oe_kanban_action oe_kanban_action_' + node.tag;
                    }
                    break;
            }
            if (node.children) {
                for (var i = 0, ii = node.children.length; i < ii; i++) {
                    this.transform_qweb_template(node.children[i]);
                }
            }
        },
        
        /*
         *  postprocessing of fields type many2many
         *  make the rpc request for all ids/model and insert value inside .oe_tags fields
         */
         postprocess_m2m_tags: function() {
             var self = this;
             if (!this.many2manys.length) {
                 return;
             }
             var relations = {};
             this.groups.forEach(function(group) {
                 group.records.forEach(function(record) {
                     self.many2manys.forEach(function(name) {
                         var field = record.record[name];
                         var $el = record.$('.oe_form_field.oe_tags[name=' + name + ']').empty();
                         if (!relations[field.relation]) {
                             relations[field.relation] = { ids: [], elements: {}, context: self.m2m_context[name]};
                         }
                         var rel = relations[field.relation];
                         field.raw_value.forEach(function(id) {
                             rel.ids.push(id);
                             if (!rel.elements[id]) {
                                 rel.elements[id] = [];
                             }
                             rel.elements[id].push($el[0]);
                         });
                     });
                 });
             });
            _.each(relations, function(rel, rel_name) {
                 var dataset = new instance.web.DataSetSearch(self, rel_name, self.dataset.get_context(rel.context));
                 call = false
                 dataset.name_get(_.uniq(rel.ids)).then(function(result) {
                     if(! call){
                         result.forEach(function(nameget) {
                             call = true
                             $(rel.elements[nameget[0]]).append('<span class="oe_tag">' + _.str.escapeHTML(nameget[1]) + '</span>');
                         });
                     }
                 });
             });
         },
        
        do_process_groups: function(groups) {
            var self = this;
            this.$el.find('table:first').show();
            this.$el.removeClass('oe_kanban_ungrouped').addClass('oe_kanban_grouped');
            this.add_group_mutex.exec(function() {
                self.do_clear_groups();
                self.dataset.ids = [];
                if (!groups.length) {
                    self.no_result();
                    return false;
                }
                self.nb_records = 0;
                var groups_array = [];
                return $.when.apply(null, _.map(groups, function (group, index) {
                    var def = $.when([]);
                    var dataset = new instance.web.DataSetSearch(self, self.dataset.model,
                        new instance.web.CompoundContext(self.dataset.get_context(), group.model.context()), group.model.domain());
                    if (self.dataset._sort) {
                        dataset.set_sort(self.dataset._sort);
                    }
                    if (group.attributes.length >= 1) {
                        def = dataset.read_slice(self.fields_keys.concat(['__last_update']), { 'limit': self.limit });
                    }
                    return def.then(function(records) {
                            self.nb_records += records.length;
                            self.dataset.ids.push.apply(self.dataset.ids, dataset.ids);
                            dataset.o2m_field = self.dataset.o2m_field
                            groups_array[index] = new instance.web_kanban.KanbanGroup(self, records, group, dataset);
                    });
                })).then(function () {
                    if(!self.nb_records) {
                        self.no_result();
                    }
                    if (self.dataset.index >= self.nb_records){
                        self.dataset.index = self.dataset.size() ? 0 : null;
                    }
                    return self.do_add_groups(groups_array);
                });
            });
        },
    })

    instance.web_kanban.KanbanGroup.include({
        
        do_add_records: function(records, prepend) {
            var self = this;
            var $list_header = this.$records.find('.oe_kanban_group_list_header');
            var $show_more = this.$records.find('.oe_kanban_show_more');
            var $cards = this.$records.find('.oe_kanban_column_cards');
            var record_length = records.length
            _.each(records, function(record) {
                if(_.keys(self.dataset.o2m_field).length){
                    var count = 0
                    _.each(self.dataset.o2m_field,function(data,index){
                        var ids = record[data.field_name];
                        var model = data.model
                        var fields = data.fields
                        self.o2m_dataset = new instance.web.DataSetSearch(self, model, {}, []);
                        self.o2m_dataset.read_slice(fields, {'domain': [['id', 'in', ids]]}).then(function(field_record){
                            
                            record[data.field_name] = field_record
                            count ++ ;
                            var rec = new instance.web_kanban.KanbanRecord(self, record);
                            if(count == _.keys(self.dataset.o2m_field).length){
                                if (!prepend) {
                                    rec.appendTo($cards);
                                    self.records.push(rec);
                                 } else {
                                     rec.prependTo($cards);
                                     self.records.unshift(rec);
                                 }
                                 if(self.records.length == record_length ){
                                    self.view.postprocess_m2m_tags();
                                }
                             }
                        })
                    })
                }else{
                    var rec = new instance.web_kanban.KanbanRecord(self, record);
                    if (!prepend) {
                        rec.appendTo($cards);
                        self.records.push(rec);
                    } else {
                        rec.prependTo($cards);
                        self.records.unshift(rec);
                    }
                }
            });
            if ($show_more.length) {
                var size = this.dataset.size();
                $show_more.toggle(record_length < size).find('.oe_kanban_remaining').text(size - this.records.length);
            }
        },
    });
 
    instance.web_kanban.KanbanRecord.include({
        do_reload: function() {
            var self = this;
            this.view.dataset.read_ids([this.id], this.view.fields_keys.concat(['__last_update'])).done(function(records) {
                _.each(self.sub_widgets, function(el) {
                    el.destroy();
                });
                self.sub_widgets = [];
                if(_.keys(self.view.dataset.o2m_field).length){
                    var count = 0
                    _.each(self.view.dataset.o2m_field,function(data,index){
                        var ids = records[0][data.field_name];
                        var fields = data.fields
                        var model = data.model
                        self.o2m_dataset = new instance.web.DataSetSearch(self, model, {}, []);
                        self.o2m_dataset.read_slice(fields, {'domain': [['id', 'in', ids]]}).then(function(field_record){
                            count ++ ;
                            if(count == _.keys(self.view.dataset.o2m_field).length){
                                records[0][data.field_name] = field_record
                                self.set_record(records[0]);
                                self.renderElement();
                                self.init_content();
                                self.group.compute_cards_auto_height();
                                self.view.postprocess_m2m_tags();
                            }
                        });
                    });
                }else{
                    if (records.length) {
                        self.set_record(records[0]);
                        self.renderElement();
                        self.init_content();
                        self.group.compute_cards_auto_height();
                        self.view.postprocess_m2m_tags();
                    } else {
                        self.destroy();
                    }
                }
            });
        },
    });

}