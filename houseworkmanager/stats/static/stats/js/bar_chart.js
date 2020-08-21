var chart_dict = JSON.parse(document.getElementById('chart_dict').textContent);
google.charts.load("current", {packages:['corechart']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
  var data = google.visualization.arrayToDataTable(chart_dict.table);

  var view = new google.visualization.DataView(data);

  var options = {
    title: chart_dict.title,
    isStacked: true,
    legend: {position: 'top'},
  };
  var chart = new google.visualization.BarChart(document.getElementById("chart"));
  chart.draw(view, options);
}