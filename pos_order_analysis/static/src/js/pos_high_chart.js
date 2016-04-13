openerp.pos_order_analysis = function (instance) {
    var QWeb = instance.web.qweb,
         _lt = instance.web._lt;
         var _t = instance.web._t;

    instance.web.client_actions.add('pos_chart.action', 'instance.pos_high_chart');
    instance.pos_high_chart = instance.web.Widget.extend({

        template : 'PosChartWidget',

        build_widget: function() {
            return new instance.web.DateTimeWidget(this);
        },

        start : function(){
            var self = this;
            self.pos_chart_customer = new instance.web.DataSetSearch(self, 'pos.order', {}, []);
            self.pos_chart_customer.read_slice(['id','partner_id'], {'domain': [['partner_id', '!=', false],['state','=','paid']]}).done(function(records){
                   var template = "<option value=''>All</option>";
                   var duplicate_partner = []
                   _.each(records, function(res) {
                       if(duplicate_partner.indexOf(res.partner_id[0]) == -1){
                           duplicate_partner.push(res.partner_id[0])
                           template = template + '<option value=' + res.partner_id[0] + '>' + res.partner_id[1] + '</option>'
                       }
                   });
                   self.$("#pos_chart_customer").append(template)
                   self.$('#pos_chart_customer').select2();
            });
            self.pos_chart_product = new instance.web.DataSetSearch(self, 'pos.order.line', {}, []);
            self.pos_chart_product.read_slice(['id','product_id']).done(function(records){
                var template = "<option value='0'>All</option>";
                var duplicate_product = []
                _.each(records, function(res) {
                    if(duplicate_product.indexOf(res.product_id[0]) == -1){
                        duplicate_product.push(res.product_id[0])
                        template = template + '<option value=' + res.product_id[0] + '>' + res.product_id[1] + '</option>'
                    }
                });
                self.$("#pos_chart_product").append(template)
                self.$('#pos_chart_product').select2();
            });

            self.from_date_widget = this.build_widget();
            self.from_date_widget.appendTo(this.$el.find(".datetimepicker_from_date"));

            self.to_date_widget = this.build_widget();
            self.to_date_widget.appendTo(this.$el.find(".datetimepicker_to_date"));

            $("#search_button").click(function(){
                self.display_chart_data();
            });
            self.$("#pos_chart_product").change(function(){
                self.display_chart_data();
            });
            self.$("#pos_chart_customer").change(function(){
                self.display_chart_data();
            });
        },
        
        display_chart_data : function(){
            var self = this;
            date_start = self.from_date_widget.get_value();
            end_date = self.to_date_widget.get_value();
            partner_id = $("#pos_chart_customer").val();
            product_id = $("#pos_chart_product").val();
            if(!product_id){
                product_id = false;
            }else if(product_id[0] == 0){
                product_id = false;
            }
            if(date_start && end_date){
                if(date_start > end_date){
                    $("#pos_graph_container").html("<h4 class='empty_record'>Records Not Found.</h4>");
                    self.do_warn(_t('Start Date greater than end date'),_t('Please select less than date.'));
                    return false;
                }
                self.session.rpc("/web/pos_order_date", {'start_date':date_start,'end_date':end_date,'partner_id':partner_id,'product_id':product_id}).done(function(callback){
                    if(callback[1].length != 0 ){
                        var max_x_axis = (callback[1].length > 7  ) ? 6 : callback[1].length -1 ;
                        $('#pos_graph_container').highcharts({
                            chart : {
                                height: 500,
                                zoomType: 'x'
                            },
                            title: {
                                text: _t('Pos Orders Analysis')
                            },
                            xAxis: {
                                categories: callback[1],
                                title: {
                                    text: _t("Product"),
                                },
                                min: 0,
                                max:max_x_axis
                            },
                            scrollbar: {
                                enabled: true,
                                height: 30,
                            },
                            yAxis: {
                                title: {
                                    text: _t("Total Consumption"),
                                    align: 'middle'
                                },
                                labels: {
                                    overflow: 'justify'
                                }
                            },
                            plotOptions: {
                                spline: {
                                    turboThreshold: 500000
                                },
                                column: {
                                    turboThreshold: 500000
                                },
                                pie: {
                                    turboThreshold: 500000
                                },
                            },
                            series: callback[0]
                        });
                    }else{
                        $("#pos_graph_container").html("<h4 class='empty_record'>Records Not Found.</h4>");
                        self.do_warn(_t('Records Not Found.'),'');
                    }
                });
            }else{
                $("#pos_graph_container").html("<h1 class='empty_record'>Records Not Found.</h1>");
                var start_date_str = _t('Start Date');
                var end_date_str = _t('End Date');
                if(!date_start && ! end_date){
                    self.do_warn(_t("The following fields are invalid:"),"<ul><li>"+start_date_str +"</li><li>" + end_date_str + "</li></ul>");
                }else if(!date_start){
                    self.do_warn(_t("The following fields are invalid:"),"<ul><li>"+start_date_str+"</li></ul>");
                }else if(!end_date){
                    self.do_warn(_t("The following fields are invalid:"),"<ul><li>"+end_date_str+"</li></ul>");
                }
            }
        }

    });

};
// vim:et fdc=0 fdl=0
