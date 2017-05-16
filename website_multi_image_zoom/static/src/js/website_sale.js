odoo.define('website_multi_image_zoom.website_sale', function(require) {

    var ajax = require('web.ajax');
    $(document).ready(function() {
        $('.oe_website_sale').each(function() {
            var demo = '<div class="xzoom-container"><img class="xzoom" id="xzoom-default" xoriginal="' + $('#ex1').find('img').attr("src") + '" style="width: 300px; height: 350px;" src="' + $('#ex1').find('img').attr("src") + '"/></div>';
            $('#ex1 span').html(demo);
            var oe_website_sale = this;

            function price_to_str(prices) {
            	var price = prices;
                price = Math.round(price * 100) / 100;
                var dec = Math.round((price % 1) * 100);
                return price +
                    (dec
                        ? ''
                        : '.0') +
                    (dec % 10
                        ? ''
                        : '0');
            }

            $(oe_website_sale).on('change', 'input.js_variant_change, select.js_variant_change, ul[data-attribute_value_ids]', function(ev) {
                var $ul = $(ev.target).closest('ul.js_add_cart_variants');
                var $parent = $ul.closest('.js_product');
                var product_id = $parent.find('input.product_id').first().val();
                var $img = $(this).closest('tr.js_product, .oe_website_sale').find('span[data-oe-model^="product."][data-oe-type="image"] img:first, img.product_detail_img');
                if ($('#variant_img_display').val()) {
                    if (product_id) {
                        ajax.jsonRpc("/get_variant_images", 'call', {
                            'product_id': product_id
                        }).then(function(data) {
                            var str = '<li><img onclick="pro_img_click(this)" class="xzoom-gallery" width="80" src="/web/image/product.product/' + product_id + '/image" xpreview="/web/image/product.product/' + product_id + '/image"/></li>';
                            var pro_imgs = data.product_rec;
                            for (var i = 0; i < pro_imgs.length; i++) {
                                str += '<li><img onclick="pro_img_click(this)" class="xzoom-gallery" width="80" src="/web/image/product.image/' + pro_imgs[i] + '/image" xpreview="/web/image/product.image/' + pro_imgs[i] + '/image" /></li>';
                            }
                            var first_append = "<div id='carousel-custom' class='carousel slide'><ol class='carousel-indicators'>" + str + "</ol></div>";
                            $("#carousel-custom").remove();
                            $('#thumb_img_add').append(first_append);
                        });
                    }
                } else {
                    $img.attr("src", "/website/image/product.template/" + $('#product_img_display').val() + "/image");
                }
            });

            $('ul.js_add_cart_variants', oe_website_sale).each(function() {
                $('input.js_variant_change, select.js_variant_change', this).first().trigger('change');
            });

        });
    });
});
