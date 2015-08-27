$(document).ready(function() {
    $('.oe_website_sale').each(function() {
        var oe_website_sale = this;
        function price_to_str(price) {
            price = Math.round(price * 100) / 100;
            var dec = Math.round((price % 1) * 100);
            return price + (dec ? '' : '.0') + (dec % 10 ? '' : '0');
        }

        $(oe_website_sale).on('change', 'input.js_variant_change, select.js_variant_change, ul[data-attribute_value_ids]', function(ev) {
        	var $ul = $(ev.target).closest('ul.js_add_cart_variants');
            var $parent = $ul.closest('.js_product');
            var product_id = $parent.find('input.product_id').first().val();
            var $img = $(this).closest('tr.js_product, .oe_website_sale').find('span[data-oe-model^="product."][data-oe-type="image"] img:first, img.product_detail_img');

            if ($('#variant_img_display').val()) {
                if (product_id) {
                    openerp.jsonRpc("/get_variant_images", 'call', {'product_id': product_id}).then(function(data) {
                        var str = '<li><img onClick="pro_img_click(this)" class="image_thumb img-responsive" src="/website/image/product.product/' + product_id + '/image"/></li>';
                        var pro_imgs = data['product_rec'];
                        for (i = 0; i < pro_imgs.length; i++) {
                            str += '<li><img onClick="pro_img_click(this)" class="image_thumb img-responsive" src="/website/image/product.image/' + pro_imgs[i] + '/image"/></li>';
                        }
                        var first_append = "<div id='carousel-custom' class='carousel slide'><ol class='carousel-indicators'>" + str + "</ol></div>"
                        $("#carousel-custom").remove();
                        $('#thumb_img_add').append(first_append);
                    });
                }
            }
            else {
                $img.attr("src", "/website/image/product.template/" + $('#product_img_display').val() + "/image");
            }
            var wi = $(window).width();
            if (wi >= 980) {
            	$img.attr("id", "image2"); // Give Id to image
                $('#image2').addimagezoom({
                    zoomrange: [2, 10],
                    magnifiersize: [350, 350],
                    magnifierpos: 'right',
                    cursorshade: true,
                });
            }
        });

        $('ul.js_add_cart_variants', oe_website_sale).each(function () {
            $('input.js_variant_change, select.js_variant_change', this).first().trigger('change');
        });

    });
});