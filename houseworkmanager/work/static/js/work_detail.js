var ctx = document.getElementById("charts");
var myWorkChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels:label,
        datasets: [{
            label: 'グラフ',
            backgroundColor: '#20B2AA',
            data: datasets
        }],
    },
    options: {
        title: {
            display: true,
            text: '実行割合'
        }
    }
);