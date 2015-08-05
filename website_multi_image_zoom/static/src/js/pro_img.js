//Method to change Main product image when click on thumbnail image
$(".image_thumb").click(function () {
    $('#ex1').children().children().attr("src", this.src);
    var wi = $(window).width();
    if (wi >= 980){
        $('#ex1').children().children().attr("id","image2"); // Give Id to image
        $('#image2').addimagezoom({
            zoomrange : [ 2, 10 ],
            magnifiersize : [ 350, 350 ],
            magnifierpos : 'right',
            cursorshade : true,
        });
    }
});
