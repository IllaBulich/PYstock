Highcharts.chart('container', {

    title: {
        text: 'Прогнозирование спроса',
        
    },

    yAxis: {
        title: {
            text: 'Количество едениц'
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