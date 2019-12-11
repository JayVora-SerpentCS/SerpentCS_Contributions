odoo.define('web_groupby_expand.web_groupby_expand', function(require) {

var core = require('web.core');
var ListRenderer = require('web.ListRenderer');
var AbstractController = require('web.AbstractController');
var config = require('web.config');
var _t = core._t;
var QWeb = core.qweb;

var HEADING_COLUMNS_TO_SKIP_IN_GROUPS = 2

ListRenderer.include({

    init: function (parent, state, params) {
        var self = this;
        var res = this._super.apply(this, arguments);
        this.expand = false;
        this.expand_btn = false;
        this.in_expand = false;
        return res;
    },

    render_auto_groups: function() {
        var self = this;
        var is_grouped = !!self.state.groupedBy.length;
        if (is_grouped) {
            self.expand = true;
            _.each(self.state.data, function(group) {
                if(group){
                    self.trigger_up('toggle_group', {group: group});
                }
            })
        }
    },

    _renderGroupRow: function (group, groupLevel) {
        var self = this;
        var res = this._super.apply(this, arguments);
        if (self.expand) {
            if(self.in_expand){
                if(group.isOpen==false){
                    self.trigger_up('toggle_group', {group: group});
                }
            }
        }
        return res;
    },

    _onRowClicked: function (event) {
        this.expand = false;
        return this._super(event)
    },

});

AbstractController.include({
    _renderSwitchButtons: function () {
        var res = this._super();
        var self = this;
        var totalViews = _.filter(self.actionViews, {multiRecord: self.isMultiRecord});
        if (totalViews.length <= 1 ) {
            var template = 'ControlPanel.SingleViewSwitchButtons';
            res = $(QWeb.render(template, {
                this:self
            }));
        }
        var oe_list_expand;
        _.each(res, function(rec){
            if (rec.id == 'expand_icon'){
                oe_list_expand = $(rec);
            }
        })
        if(self.viewType !== 'list'){
            oe_list_expand.hide();
        } else if(self.viewType === 'list'){
            if(self.renderer.state.groupedBy.length > 0){
                oe_list_expand.show();
            } else {
                oe_list_expand.hide();
            }
            oe_list_expand.unbind('click').bind('click', function() {
                var is_grouped = !!self.renderer.state.groupedBy.length;
                if (is_grouped) {
                    if ($(this).hasClass('fa-expand')){
                        self.renderer.in_expand = true;
                        $(this).removeClass('fa-expand');
                        $(this).addClass('fa-compress');
                    }else{
                        self.renderer.in_expand = false;
                        $(this).addClass('fa-expand');
                        $(this).removeClass('fa-compress');
                    }
                    self.renderer.render_auto_groups();
                }
            });
        }
        return res;
    },
    reload: async function (params) {
        var self = this;
        this._super(params).then(function(){
            if(self.viewType==='list'){
                $('#expand_icon').show()
                if(params.groupBy){
                    if(params.groupBy.length > 0){
                        $('#expand_icon').show()
                    } else if (params.groupBy.length == 0){
                        $('#expand_icon').hide()
                    }
                }else {
                    if(self.renderer.isGrouped){
                         $('#expand_icon').show()
                    } else {
                         $('#expand_icon').hide()
                    }
                }
            }
            if(self.viewType!=='list'){
                $('#expand_icon').hide()
            }
        })
    },
});

});
