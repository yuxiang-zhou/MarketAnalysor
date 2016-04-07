angular.module('marketApp').directive('stockchart', function() {
  return {
    templateUrl: 'scripts/components/stockchart/stockchart.html',
    replace: true,
    restrict: 'E',
    scope: {
      url: '=',
      plotid: '@',
      title: '@',
      annotation: '='
    },
    link: function($scope, elem, attrs) {

      // chart plot def
      function plot(seriesOptions, axesOptions) {
        elem.highcharts('StockChart', {

          rangeSelector: {
            selected: 4
          },

          tooltip: {
            valueDecimals: 2,
            shared : true
          },

          yAxis: axesOptions,
          xAxis: {
            tickPixelInterval: 1
          },
          series: seriesOptions
        });
      }

      var jqxhr = $.getJSON($scope.url, function(data) {
        var i, j, len;

        var history = [];

        // data processing
        for (i = 0, len = data.length; i < len; i++) {
          var h = data[i]['fields'];
          var strDate = new Date(Date.parse(h.pub_date));
          var wk4limit = new Date(Date.parse(h.pub_date));
          var wk13limit = new Date(Date.parse(h.pub_date));
          var wk4_moving_avg = 0;
          var wk13_moving_avg = 0;

          wk4limit.setDate(wk4limit.getDate()-28);
          wk13limit.setDate(wk13limit.getDate()-91);

          for (j = i; j < len; j++) {
            var th = data[j]['fields']
            var curDate = new Date(Date.parse(th.pub_date));
            if (curDate > wk4limit){
              wk4_moving_avg += th.Close;
            } else {
              break;
            }
          }
          wk4_moving_avg /= (j-i);

          for (j = i; j < len; j++) {

            var th = data[j]['fields']
            var curDate = new Date(Date.parse(th.pub_date));
            if (curDate > wk13limit){
              wk13_moving_avg += th.Close;
            } else {
              break;
            }
          }

          wk13_moving_avg /= (j-i);

          history.push([
            strDate,
            h.Close,
            wk4_moving_avg,
            wk13_moving_avg,
            h.Volumn
          ]);

        }

        // data settings
        var seriesOptions = [];
        var axesOptions = [];

        labels = ['Close', '4 wk moving avg', '13 wk moving avg', 'Volumn'];
        $.each(labels, function(index, value){

          var hist = [];
          $.each(history, function(hi, hv){
            hist.push([hv[0].getTime(), hv[index+1]]);
          });

          var lastentry = index == labels.length -1;
          seriesOptions.push({
            name: value,
            data: hist.reverse(),
            shadow : true,
            type: lastentry ? 'column' : '',
            yAxis: lastentry ? 2 : 0,
            id: index == 0 ? 'dataseries' : undefined
          });
        });

        // news label settings
        if($scope.annotation) {
          var newslistasc = [];
          $scope.annotation.reverse();
          $.each($scope.annotation, function(ni, news){
            newslistasc.push({
              x : new Date(news.pub_date).getTime(),
              title : news.title[0],
              text : news.title,
              events: {
                click: function(){window.location.href = news.url;},
              },
            });
          });
          $scope.annotation.reverse();

          seriesOptions.push({
            name: 'news',
            type : 'flags',
            shadow : true,
            yAxis: 0,
            data : newslistasc,
            onSeries : 'dataseries',
            shape : 'circlepin',
            width : 16
          });

        }

        // axis settings
        axesOptions = [{
          title: {
            text: $scope.title
          },
          height: '70%',
          lineWidth: 1,
          tickPixelInterval: 1
        }, {
          opposite: false,
          title: {
            text: 'Changes'
          },
          labels: {
            align: 'right',
            x: 30,
            formatter:function(){
              var max=this.axis.linkedParent.dataMax,
                min=this.axis.linkedParent.dataMin,
                mid=(max+min) / 2.0;
              return ((this.value-mid)/(mid)*100).toFixed(0) + ' %';
            }
          },
          height: '70%',
          linkedTo:0,
          lineWidth: 1,
          tickPixelInterval: 1
        }, {
          title: {
            text: 'Volume'
          },
          top: '75%',
          height: '25%',
          offset: 0,
          lineWidth: 1,
          tickPixelInterval: 1
        },{
          top: '75%',
          height: '25%',
          offset: 0,
          lineWidth: 1,
          opposite: false
        }];

        elem.removeClass('loader');
        plot(seriesOptions, axesOptions);
      });

    }
  }
});
