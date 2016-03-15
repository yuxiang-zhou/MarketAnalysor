$(function(){
  $('#btnSearch').click(function(){
    window.location.href = "/detail/" + $("#txtSearch").val();
  });

  $("#txtSearch").keyup(function(event){
    if(event.keyCode == 13){
        $("#btnSearch").click();
    }
  });

  setInterval(function(){location.reload();}, 5 * 60 * 1000);

});

function plot(url, eleid, title) {
  console.log('Loading Chat Data');
  var jqxhr = $.getJSON(url, function(data) {
    var h, history, i, len, strDate, volumnChart;

    history = [];

    for (i = 0, len = data.length; i < len; i++) {
      h = data[i]['fields'];
      strDate = new Date(Date.parse(h.pub_date));
      history.push([
        strDate, h.Close, undefined, undefined,h.Volumn, undefined, undefined
      ]);
    }

    var data = new google.visualization.DataTable();
    data.addColumn('date', 'Date');
    data.addColumn('number', 'Price ('+title+'):');
    data.addColumn('string', 'Price Title');
    data.addColumn('string', 'Price Text');
    data.addColumn('number', 'Volumn ('+title+'):');
    data.addColumn('string', 'Volumn Title');
    data.addColumn('string', 'Volumn Text');
    data.addRows(history);

    var container = document.getElementById(eleid);
    container.className = "candlestickChartContainer";
    var chart = new google.visualization.AnnotationChart(
      container
    );

    var pastdate = new Date();
    pastdate.setFullYear(pastdate.getFullYear()-1);

    var options = {
      displayAnnotations: true,
      scaleColumns: [0, 1],
      scaleType: 'allmaximized',
      fill: 25,
      zoomStartTime: pastdate
    };

    chart.draw(data, options);

  });
}
