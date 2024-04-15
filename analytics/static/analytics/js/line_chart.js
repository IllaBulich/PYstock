
Highcharts.chart('container_1', {

    title: {
        text: 'Статистика поступленей',
        
    },

    yAxis: {
        title: {
            text: 'Общяя стоймасть закупак (BYN)'
        }
    },

    xAxis: {
        categories: chartsData.cost_chart.dades_list
    },

    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle'
    },

    plotOptions: {
        
    },

    series: chartsData.cost_chart.series,


});
Highcharts.chart('container_2', {

    title: {
        text: 'Статистика поступленей',
        
    },

    yAxis: {
        title: {
            text: 'Общяя количество'
        }
    },

    xAxis: {
        categories: chartsData.quantity_chart.dades_list
    },

    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle'
    },

    plotOptions: {
        
    },

    series: chartsData.quantity_chart.series,


});

Highcharts.chart('container_3', {

    title: {
        text: 'Статистика сбыта',
        
    },

    yAxis: {
        title: {
            text: 'Общий обём сбыта (BYN)'
        }
    },

    xAxis: {
        categories: chartsData.cost_chart.dades_list
    },

    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle'
    },

    plotOptions: {
        
    },

    series: chartsData.cost_chart.series,


});

Highcharts.chart('container_4', {

    title: {
        text: 'Статистика сбыта',
        
    },

    yAxis: {
        title: {
            text: 'Общий обём сбыта'
        }
    },

    xAxis: {
        categories: chartsData.quantity_chart.dades_list
    },

    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle'
    },

    plotOptions: {
        
    },

    series: chartsData.quantity_chart.series,


});

