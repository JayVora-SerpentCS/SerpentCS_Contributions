$( document ).ready(function () {
    function myFunction () {
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

$(document).on("click",".check_required_fields", function(){
    var flag = 0;
    var field_list = ['business_categ_id','category_name','relation_id','name','phone','email','description'];

    field_list.forEach(function (e) {
        if ($(`input[name='${e}']`).val() == '') {
            $(`input[name='${e}']`).css({ 'border': '1px solid red' });
            return false;
        }
        else{
            $(`input[name='${e}']`).css({ 'border': '' });
        }
    });
     

});

$(document).on("change", ".select_business_categ", function () {
    if ($(this).val() == -1) {
        $(".form_so_new_shipp").removeClass("d-none");
        $(".form_so_new_shipp input").prop('required', true);
    } else {
        $(".form_so_new_shipp").addClass("d-none");
        $(".form_so_new_shipp input").prop('required', false);
    }
});
