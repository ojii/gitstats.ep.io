var PyHighCharts = new Class({
    initialize: function(options){
        this.container = $(options.container);
        this.charts = options.charts;
        this.charts.each(this.init_chart, this);
    },
    
    init_chart: function(data, index){
    	var div = new Element('div', {'class': 'chart', 'id': 'chart' + index});
    		div.inject(this.container, 'bottom');
    	data['chart']['renderTo'] = 'chart' + index;
		new Highcharts.Chart(data);
    }
});
