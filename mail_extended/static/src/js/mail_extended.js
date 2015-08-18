openerp.mail_extended = function(openerp) {
    var _t = openerp.web._t;
    var initial_mode = "view"
    var QWeb = openerp.web.qweb;

    openerp.mail.ThreadMessage.include({
        bind_events: function () {
            var self = this;
            this._super();
            // header icons bindings
            this.$el.find('.oe_msg_forward').on('click', this.on_forward_message);
        },
        on_forward_message: function (default_composition_mode) {
            var self = this
            messages = []
            attachment_ids = []
            var msg = false
            _.each(self.attachment_ids, function (attachment) {
                    attachment_ids.push(attachment.id)
            });
            var values = new openerp.web.Model('mail.message').call('forward_message', [[this.id], attachment_ids])
            values.done(function(vals) {
                console.log("valsvalsvalsvalsvals",vals)
                action = {
                    'type': 'ir.actions.act_window',
                    'res_model': 'mail.compose.message',
                    'view_mode': 'form',
                    'view_type': 'form',
                    'views': [[false, 'form']],
                    'target': 'new',
                    'context' : vals
                }
                self.do_action(action);
            })
        },
    })
};
