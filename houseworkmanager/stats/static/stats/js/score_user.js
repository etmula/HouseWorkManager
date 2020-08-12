var score_user_data = JSON.parse(document.getElementById('score_user_data').textContent);

google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
  var data = google.visualization.arrayToDataTable(score_user_data);

  var options = {
    title: 'Score-User Line Chart',
    legend:{position: 'top' },
  };

  var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

  chart.draw(data, options);
}