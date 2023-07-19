odoo.define('pos_security_dialog.models', function (require) {
    "use strict";

    var models = require('point_of_sale.models');

    models.load_fields("res.company", ['security_key']);

});
