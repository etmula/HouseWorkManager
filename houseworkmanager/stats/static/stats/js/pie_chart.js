var chart_dict = JSON.parse(document.getElementById('chart_dict').textContent);

google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {

  var data = google.visualization.arrayToDataTable(chart_dict.table);

  var options = {
    title: chart_dict.title,
    legend: {position: 'top'}
  };

  var chart = new google.visualization.PieChart(document.getElementById('chart'));

  chart.draw(data, options);
}