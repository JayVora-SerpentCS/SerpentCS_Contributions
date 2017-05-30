odoo.define('project_team.form_rel', function (require) {
"use strict";

var Form_Relation = require('web.form_relational');
var core = require('web.core');
var common = require('web.form_common');
var _t = core._t;

var COMMANDS = common.commands;

Form_Relation.AbstractManyField.include({
get_value: function() {
        var self = this,
            is_one2many = this.field.type === "one2many",
            not_delete = this.options.not_delete,
            starting_ids = this.starting_ids.slice(),
            replace_with_ids = [],
            add_ids = [],
            command_list = [],
            index = 0;

        _.each(this.get('value'), function (id) {
            index = starting_ids.indexOf(id);
            if (index !== -1) {
                starting_ids.splice(index, 1);
            }
            var record = self.dataset.get_cache(id);
            if (!_.isEmpty(record.changes)) {
                var values = _.clone(record.changes);
                // format many2one values
                for (var k in values) {
                    if (values[k] instanceof Array && values[k].length === 2 && typeof values[k][0] === "number" && typeof values[k][1] === "string") {
                        values[k] = values[k][0];
                    }
                }
                if (record.to_create) {
                    command_list.push(COMMANDS.create(values));
                } else {
                    command_list.push(COMMANDS.update(record.id, values));
                }
                if (!is_one2many || not_delete || self.dataset.delete_all) {
                    replace_with_ids.push(id);
                }
                return;
            }
            if (!is_one2many || not_delete || self.dataset.delete_all) {
                replace_with_ids.push(id);
            } else {
                command_list.push(COMMANDS.link_to(id));
            }
        });
        if ((!is_one2many || not_delete || self.dataset.delete_all) && (replace_with_ids.length || starting_ids.length)) {
            _.each(command_list, function (command) {
                if (command[0] === COMMANDS.UPDATE) {
                    replace_with_ids.push(command[1]);
                }
            });
            command_list.unshift(COMMANDS.replace_with(replace_with_ids));
        }

        _.each(starting_ids, function(id) {
            if (is_one2many && !not_delete) {
                command_list.push(COMMANDS.delete(id));
            } else if (is_one2many && !self.dataset.delete_all) {
                command_list.push(COMMANDS.forget(id));
            }
        });

        return command_list;
    },
    });
});
