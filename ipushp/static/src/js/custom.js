odoo.define('ipushp.ipushp', function (require) {
    var ajax = require('web.ajax');
	$(document).on("change", ".select_business_categ", function(){
        if ($(this).val() == -1){
            $(".form_so_new_shipp").removeClass("hidden");
            $(".form_so_new_shipp input").prop('required',true);
        }
        else{
            $(".form_so_new_shipp").addClass("hidden");
            $(".form_so_new_shipp input").prop('required',false);
        }
    });
});