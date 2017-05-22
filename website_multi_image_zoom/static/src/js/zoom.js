// Zoom
$(window).load(function() {
    var isTouchSupported = 'ontouchstart' in window;

    if (isTouchSupported) {
        $('.xzoom').each(function() {
            var xzoom = $(this).data('xzoom');
            xzoom.eventunbind();
        });
        $('.xzoom').each(function() {
            var xzoom = $(this).data('xzoom');
            $(this).hammer().on("tap", function(event) {
                event.pageX = event.gesture.center.pageX;
                event.pageY = event.gesture.center.pageY;
                var s = 1;

                xzoom.eventmove = function(element) {
                    element.hammer().on('drag', function(e) {
                        e.pageX = e.gesture.center.pageX;
                        e.pageY = e.gesture.center.pageY;
                        xzoom.movezoom(e);
                        e.gesture.preventDefault();
                    });
                };

                xzoom.eventleave = function(element) {
                    element.hammer().on('tap', function(ee) {
                        xzoom.closezoom();
                    });
                };
                xzoom.openzoom(event);
            });
        });
    }
    var wi = $(window).width();
    if (wi >= 980) {
        $("#ex1").hover(function() {
                $('.xzoom, .xzoom-gallery').xzoom({
                    zoomWidth: 450,
                    title: true,
                    tint: '#333',
                });
            },
            function() {
                $('#ex1').children().children().removeAttr("id"); // remove all attributes
            });
    } else {
        $('#ex1').children().children().removeAttr("id"); // remove all attributes
    }
});

//Method to change Main product image when click on thumbnail image
function pro_img_click(proimg) {
    var demo = '<div class="xzoom-container"><img class="xzoom" id="xzoom-default" xoriginal="' + proimg.src + '" style="width: 300px; height: 350px;" src="' + proimg.src + '"/></div>';
    $('#ex1 span').html(demo);
};

//Show Model
(function full_img(sample) {
    var wi = $(window).width();
    if (wi < 980) {
        var img_bin = $(sample).find("img");
        $('#modal_img').attr('src', $(img_bin).attr("src"));
        $('#img_modal').modal('show');
    }
})();
