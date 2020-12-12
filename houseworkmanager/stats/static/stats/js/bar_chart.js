google.charts.load("current", {packages:['corechart']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
  var chart_dict = JSON.parse(document.getElementById('chart_dict').textContent);
  document.getElementById('chart_dict').remove()
  var data = google.visualization.arrayToDataTable(chart_dict.table);

  var view = new google.visualization.DataView(data);

  var options = {
    title: chart_dict.title,
    isStacked: true,
    legend: {position: 'top'},
  };
  var chart = new google.visualization.BarChart(document.getElementById(chart_dict.id));

  chart.draw(view, options);
}