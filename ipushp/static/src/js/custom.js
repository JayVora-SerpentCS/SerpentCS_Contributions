odoo.define('ipushp.ipushp', function (require) {
    var ajax = require('web.ajax');
    $( document ).ready(function() {
    	console.log("Ready page");
    	function myFunction() {
    		console.log("function called");
    		    var input, filter, ul, li, a, i;
    		    input = document.getElementById("myInput");
    		    filter = input.value.toUpperCase();
    		    ul = document.getElementById("myUL");
    		    li = ul.getElementsByTagName("li");
    		    for (i = 0; i < li.length; i++) {
    		        a = li[i].getElementsByTagName("a")[0];
    		        if (a.innerHTML.toUpperCase().indexOf(filter) > -1) {
    		            li[i].style.display = "";
    		        } else {
    		            li[i].style.display = "none";

    		        }
    		    }
    		}
    });
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