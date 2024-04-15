Highcharts.chart('container_1', {

    title: {
        text: 'Статистика поступления и сбыта',
        
    },

    yAxis: {
        title: {
            text: 'Общий обём в (BYN)'
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
        text: 'Статистика поступления и сбыта',
        
    },

    yAxis: {
        title: {
            text: 'Общий обём в шт.'
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

