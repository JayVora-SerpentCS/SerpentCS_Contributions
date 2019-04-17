odoo.define('web_groupby_expand.web_groupby_expand', function(require) {

    var core = require('web.core');
    var ListRenderer = require('web.ListRenderer')
    var AbstractController = require('web.AbstractController');
    var _t = core._t;

    var HEADING_COLUMNS_TO_SKIP_IN_GROUPS = 2

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
            var self = this;
            var aggregateValues = _.mapObject(group.aggregateValues, function (value) {
                return { value: value };
            });
            var $cells = this._renderAggregateCells(aggregateValues, true);
            var name = group.value === undefined ? _t('Undefined') : group.value;
            var groupBy = this.state.groupedBy[groupLevel];
            if (group.fields[groupBy.split(':')[0]].type !== 'boolean') {
                name = name || _t('Undefined');
            }
            var $th = $('<th>')
                .addClass('o_group_name')
                .text(name + ' (' + group.count + ')');
            if (this.hasSelectors) {
                $th.attr('colspan', HEADING_COLUMNS_TO_SKIP_IN_GROUPS);
            }
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
                var $lastCell = $cells[$cells.length - 1] || $th;
                $lastCell.addClass('o_group_pager').append($pager);
            }

            if (self.expand) {
                if(self.in_expand){
                    if(group.isOpen==false){
                        self.trigger_up('toggle_group', {group: group});
                    }
                }
            }

            return $('<tr>')
                .addClass('o_group_header')
                .toggleClass('o_group_open', group.isOpen)
                .toggleClass('o_group_has_content', group.count > 0)
                .data('group', group)
                .append($th)
                .append($cells);
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
                    self.expand = true;
                    self.in_expand = false;
                    self.render_auto_groups();
                    $(this).addClass('fa-expand');
                    $(this).removeClass('fa-compress');
                })
            }
            var res = this._super();
            return res
        },

        _onRowClicked: function (event) {
            this.expand = false;
            return this._super(event)
        },
    });

    AbstractController.include({
        _renderSwitchButtons: function () {
            var self = this
            var res = this._super.apply(this, arguments);
            if(this.viewType !== 'list'){
                arr = jQuery.grep(res, function( a ) {
                    if($(a)[0].className == 'btn btn-default fa fa-expand oe-list-expand'){
                        $(a).hide();
                    }
                });
            }
            return res;
        },
    });

});
