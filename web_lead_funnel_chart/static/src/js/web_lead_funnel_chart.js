/*global Highcharts*/
odoo.define("web_lead_funnel_chart.web_lead_funnel_chart", function(require) {
    "use strict";

    var core = require("web.core");
    var dataset = require("web.data");
    var Widget = require("web.Widget");
    var _t = core._t;

    var web_lead_funnel_chart = Widget.extend({
        template: "FunnelChart",
        start: function() {
            var self = this;
            var emp_child = [];
            self.crm_lead_dataset = new dataset.DataSetSearch(self, "crm.lead", {}, []);
            self.crm_lead_dataset.call("get_lead_stage_data", [
                []
            ]).done(function(callbacks) {
                $("#container").highcharts({
                    chart: {
                        type: "funnel",
                        marginRight: 100
                    },
                    title: {
                        text: _t("Lead/Opportunity Funnel Chart"),
                        x: -50
                    },
                    plotOptions: {
                        series: {
                            dataLabels: {
                                enabled: true,
                                format: "<b>{point.name}</b>({point.y:,.0f})",
                                color: "black" || (Highcharts.theme && Highcharts.theme.contrastTextColor),
                                softConnector: true
                            },
                            neckWidth: "30%",
                            neckHeight: "25%"

                            //-- Other available options
                            // height: pixels or percent
                            // width: pixels or percent
                        }
                    },
                    legend: {
                        enabled: false
                    },
                    series: [{
                        name: _t("Number Of Leads"),
                        data: callbacks
                    }]
                });
            });

        },
    });

    core.action_registry.add("web_lead_funnel_chart.funnel", web_lead_funnel_chart);

});
