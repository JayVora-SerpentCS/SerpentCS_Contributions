// Zoom init
$(window).load(function() {
    var wi = $(window).width();
    if (wi >= 980){
        $("#ex1").hover(function() {
            $('#ex1').children().children().attr("id","image2"); // Give Ids of images
            $('#image2').addimagezoom({
                zoomrange : [ 2, 10 ],
                magnifiersize : [ 350, 350 ],
                magnifierpos : 'right',
                cursorshade : true,
            });
        },
        function() {
            $('#ex1').children().children().removeAttr( "id" ); // remove all attributes
        });
    }else{
        $('#ex1').children().children().removeAttr( "id" ); // remove all attributes
    }
});

//Method to change Main product image when click on thumbnail image
function pro_img_click(proimg) {
	$('#ex1').children().children().attr("src", proimg.src);
	var wi = $(window).width();
	if (wi >= 980) {
		$('#ex1').children().children().attr("id", "image2"); // Give Id to image
		$('#image2').addimagezoom({
			zoomrange: [2, 10],
			magnifiersize: [350, 350],
			magnifierpos: 'right',
			cursorshade: true,
		});
	}
}

//Show Model
function full_img(sample){
    var wi = $(window).width();
    if (wi < 980){
        var img_bin=$(sample).find("img");
        $('#modal_img').attr('src',$(img_bin).attr("src"));
        $('#img_modal').modal('show');
    }
}

