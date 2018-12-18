odoo.define('web_groupby_expand.web_groupby_expand', function(require) {

    var core = require('web.core');
    var ListRenderer = require('web.ListRenderer')
    var ViewManager = require('web.ViewManager');
    var _t = core._t;

    ListRenderer.include({

        init: function (parent, state, params) {
            var self = this;
            this.expand = false;
            this.expand_btn = false;
            var res = this._super.apply(this, arguments);
            return res;
        },

        render_auto_groups: function() {
            var self = this;
            _.each(self.state.data, function(group) {
                if(group){
                    self.trigger_up('toggle_group', {group: group});
                }
            })

        },

        _renderGroupRow: function (group, groupLevel) {
            var self =  this
            var aggregateValues = _.mapObject(group.aggregateValues, function (value) {
                return { value: value };
            });
            var $cells = this._renderAggregateCells(aggregateValues);
            if (this.hasSelectors) {
                $cells.unshift($('<td>'));
            }
            var name = group.value === undefined ? _t('Undefined') : group.value;
            var groupBy = this.state.groupedBy[groupLevel];
            if (group.fields[groupBy.split(':')[0]].type !== 'boolean') {
                name = name || _t('Undefined');
            }
            var $th = $('<th>')
                        .addClass('o_group_name')
                        .text(name + ' (' + group.count + ')');
            var $arrow = $('<span>')
                                .css('padding-left', (groupLevel * 20) + 'px')
                                .css('padding-right', '5px')
                                .addClass('fa');
            if (group.count > 0) {
                $arrow.toggleClass('fa-caret-right', !group.isOpen)
                        .toggleClass('fa-caret-down', group.isOpen);
            }
            $th.prepend($arrow);
            if (group.isOpen && !group.groupedBy.length && (group.count > group.data.length)) {
                var $pager = this._renderGroupPager(group);
                var $lastCell = $cells[$cells.length-1];
                $lastCell.addClass('o_group_pager').append($pager);
            }
            var tr_ = $('<tr>')
                        .addClass('o_group_header')
                        .toggleClass('o_group_open', group.isOpen)
                        .toggleClass('o_group_has_content', group.count > 0)
                        .data('group', group)
                        .append($th)
                        .append($cells);
            if (self.expand) {
                if(self.in_expand){
                    if(group.isOpen==false){
                        self.trigger_up('toggle_group', {group: group});
                    }
                }
            }
            return tr_
        },

        _renderView: function () {
            var self = this;
            var is_grouped = !!this.state.groupedBy.length;
            if (is_grouped) {
                $('button#expand_icon.fa-expand').unbind('click').bind('click', function() {
                    self.expand = true;
                    self.in_expand = true;
                    self.render_auto_groups();
                    $(this).removeClass('fa-expand');
                    $(this).addClass('fa-compress');
                })
                $('button#expand_icon.fa-compress').unbind('click').bind('click', function() {
                    self.in_expand = false;
                    self.expand = true;
                    self.render_auto_groups();
                    $(this).addClass('fa-expand');
                    $(this).removeClass('fa-compress');
                })
            }
            var res = this._super();
            return res
        },

        _onRowClicked: function (event) {
            // The special_click property explicitely allow events to bubble all
            // the way up to bootstrap's level rather than being stopped earlier.
            this.expand = false;
            if (!$(event.target).prop('special_click')) {
                var id = $(event.currentTarget).data('id');
                if (id) {
                    this.trigger_up('open_record', {id:id, target: event.target});
                }
            }
        },
    });


    ViewManager.include({

        switch_mode: function(view_type, view_options) {
            var self = this;
            var res = this._super.apply(this, arguments);
            jQuery.grep(self.switch_buttons.$multi, function( a ) {
                if($(a)[0].id == 'expand_icon'){
                    if (view_type !== 'list') {
                        $(a).hide();
                    }
                    else{
                        $(a).css('display','block')
                    }
                }
            });
            return res;
        },
    });

});
