
console.log(chartsData)
console.log(chartsData.line_chart.dades_list)
console.log(chartsData.line_chart.series)


Highcharts.chart('container', {

    title: {
        text: 'Статистика поступленей',
        
    },

    yAxis: {
        title: {
            text: 'Общяя стоймасть закупак'
        }
    },

    xAxis: {
        categories: chartsData.line_chart.dades_list
    },

    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle'
    },

    plotOptions: {
        
    },

    series: chartsData.line_chart.series,

    

});