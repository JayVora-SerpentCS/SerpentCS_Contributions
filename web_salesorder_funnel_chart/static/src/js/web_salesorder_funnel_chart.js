odoo.define('web_salesorder_funnel_chart.web_salesorder_funnel_chart', function (require) {
"use strict";

    var core = require('web.core');
    var dataset = require("web.data");
    var Widget = require('web.Widget');
    var _t = core._t;

    var web_salesorder_funnel_chart = Widget.extend({
        template: 'FunnelChart',
        start: function(){
            var self = this;
            var emp_child = []
            self.crm_sale_order_dataset = new dataset.DataSetSearch(self, 'sale.order', {}, []);
            self.crm_sale_order_dataset.call('get_sale_order_stage_data',[[]]).done(function(callbacks){
                $('#container').highcharts({
                    chart: {
                        type: 'funnel',
                        marginRight: 100
                    },
                    title: {
                        text: _t('Sales Order Funnel Chart'),
                        x: -50
                    },
                    plotOptions: {
                        series: {
                            dataLabels: {
                                enabled: true,
                                format: '<b>{point.name}</b> ({point.y:,.0f})',
                                color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black',
                                softConnector: true
                            },
                            neckWidth: '30%',
                            neckHeight: '25%'

                            //-- Other available options
                            // height: pixels or percent
                            // width: pixels or percent
                        }
                    },
                    legend: {
                        enabled: false
                    },
                    series: [{
                        name: _t('Number Of Sales Order'),
                        data: callbacks
                    }]
                });
            });

        },
    });
    core.action_registry.add('web_salesorder_funnel_chart.funnel_sale', web_salesorder_funnel_chart);

});
