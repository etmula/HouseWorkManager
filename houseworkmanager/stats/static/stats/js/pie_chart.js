google.charts.load("current", {packages:['corechart']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
  var chart_dict = JSON.parse(document.getElementById('chart_dict').textContent);
  document.getElementById('chart_dict').remove()
  var data = google.visualization.arrayToDataTable(chart_dict.table);

  var options = {
    title: chart_dict.title,
    legend: {position: 'top'}
  };

  var chart = new google.visualization.PieChart(document.getElementById(chart_dict.id));

  chart.draw(data, options);
}