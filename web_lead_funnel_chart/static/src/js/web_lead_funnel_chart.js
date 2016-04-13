openerp.web_lead_funnel_chart = function(instance){

    var QWeb = instance.web.qweb;
    var _t = instance.web._t,
        _lt = instance.web._lt;
    
    instance.web.client_actions.add('web_lead_funnel_chart.funnel','instance.web_lead_funnel_chart');
    instance.web_lead_funnel_chart = instance.Widget.extend({

        template: 'FunnelChart',

        init:function(data){
            this._super(data);
        },

        start: function(){
            var self = this
            var emp_child = []
            self.lead_data = new instance.web.DataSetSearch(self, 'crm.lead', {}, []);
            self.lead_data.call('get_lead_stage_data',[[]]).done(function(callbacks){
                $('#container').highcharts({
                    chart: {
                        type: 'funnel',
                        marginRight: 100
                    },
                    title: {
                        text: _t('Lead/Opportunity Funnel Chart'),
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
                        name: _t('Number Of Leads'),
                        data: callbacks
                    }]
                });
            })

        }
    })

}
