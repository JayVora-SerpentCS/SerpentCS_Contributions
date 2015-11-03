openerp.pos_rounding = function (instance) {
    var QWeb = instance.web.qweb;
    var _t = instance.web._t;
    var module = instance.point_of_sale;

    module.Order = module.Order.extend({
        cal_rounding_price :function(price){
            return Math.round(price*20)/20;
        },
        getTotalTaxIncluded: function() {
            var total = this.getTotalTaxExcluded() + this.getTax();
            return Math.round(total*20)/20
        },
    });

    module.ProductListWidget.include({
        renderElement: function() {
            var self = this;
            var el_str  = openerp.qweb.render(this.template, {widget: this});
            var el_node = document.createElement('div');
                el_node.innerHTML = el_str;
                el_node = el_node.childNodes[1];
            if(this.el && this.el.parentNode){
                this.el.parentNode.replaceChild(el_node,this.el);
            }
            this.el = el_node;
            var list_container = el_node.querySelector('.product-list');
            var currentOrder = self.pos.get('selectedOrder'); 
            for(var i = 0, len = this.product_list.length; i < len; i++){
                this.product_list[i].price = currentOrder.cal_rounding_price(this.product_list[i].price)
                var product_node = this.render_product(this.product_list[i]);
                product_node.addEventListener('click',this.click_product_handler);
                list_container.appendChild(product_node);
            };
        },
    });

    module.Orderline =  module.Orderline.extend({
        get_display_price: function(){
            return Math.round(this.get_base_price()*20)/20;
        },
    });

};
