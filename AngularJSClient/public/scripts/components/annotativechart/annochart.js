angular.module('marketApp').directive('annochart', function() {
  return {
    templateUrl: 'scripts/components/annotativechart/annochart.html',
    replace: true,
    restrict: 'E',
    scope: {
      url: '=',
      plotid: '@',
      title: '@'
    },
    link: function($scope, elem, attrs){
      google.charts.setOnLoadCallback(drawCharts);

      function plot(url, eleid, title) {
        console.log('Loading Chat Data');
        var jqxhr = $.getJSON(url, function(data) {
          var h, history, i, j, len, strDate, volumnChart;

          history = [];


          for (i = 0, len = data.length; i < len; i++) {
            h = data[i]['fields'];
            var strDate = new Date(Date.parse(h.pub_date));
            var wk4limit = strDate;
            var wk13limit = strDate;
            var wk4_moving_avg = 0;
            var wk13_moving_avg = 0;

            wk4limit.setDate(wk4limit.getDate()-28);
            wk13limit.setDate(wk13limit.getDate()-91);


            for (j = i; j >= 0; j--) {
              th = data[j]['fields']
              var curDate = new Date(Date.parse(th.pub_date));
              if (curDate > wk4limit){
                wk4_moving_avg += th.Close;
              } else {
                break;
              }
            }
            wk4_moving_avg /= (i-j);

            for (j = i; j >= 0; j--) {
              th = data[j]['fields']
              var curDate = new Date(Date.parse(th.pub_date));
              if (curDate > wk13limit){
                wk13_moving_avg += th.Close;
              } else {
                break;
              }
            }
            wk13_moving_avg /= (i-j);


            history.push([
              strDate,
              h.Close, undefined, undefined,
              h.Volumn, undefined, undefined,
              wk4_moving_avg, undefined, undefined,
              wk13_moving_avg, undefined, undefined,
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
          data.addColumn('number', '4 wk moving avg:');
          data.addColumn('string', 'Volumn Title');
          data.addColumn('string', 'Volumn Text');
          data.addColumn('number', '13 wk moving avg:');
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

      function drawCharts() {
        plot($scope.url, $scope.plotid, $scope.title);
      }
    }
  }
});
