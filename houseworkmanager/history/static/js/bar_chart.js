var bar_table_dict = JSON.parse(document.getElementById('bar_table_dict').textContent);
google.charts.load("current", {packages:['corechart']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
  var bar_table_data = google.visualization.arrayToDataTable(bar_table_dict.table);

  var bar_chart_view = new google.visualization.DataView(bar_table_data);

  var bar_options = {
    title: bar_table_dict.title,
    isStacked: true,
    legend: {position: 'top'},
  };
  var bar_chart = new google.visualization.BarChart(document.getElementById("bar_chart"));
  bar_chart.draw(bar_chart_view, bar_options);
}