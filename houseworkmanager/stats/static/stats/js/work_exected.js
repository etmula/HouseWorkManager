var work_exected_data = JSON.parse(document.getElementById('work_exected_data').textContent);
google.charts.load("current", {packages:['corechart']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
  var data = google.visualization.arrayToDataTable(work_exected_data);

  var view = new google.visualization.DataView(data);

  var options = {
    title: "work-exected-column",
    isStacked: true,
    legend: {position: 'top'},
  };
  var chart = new google.visualization.BarChart(document.getElementById("columnchart_values"));
  chart.draw(view, options);
}