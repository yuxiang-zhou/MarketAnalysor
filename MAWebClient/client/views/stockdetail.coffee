# Template.stockdetail.helpers
#   StockDetail: ->
#     return this

Template.stockdetail.onRendered ->
  templateData = Template.instance().data

  jqxhr = $.getJSON( "/api/history/"+templateData.symbol, (data)->
    # construct history
    # {x:new Date(Date.parse("2015-12-01T00:00:00.000Z")),y:[Open, High, Low, Close}
    history = []
    hist_volumn = []
    for h in data
      strDate = new Date(Date.parse(h._date))
      history.push
        x: strDate
        y: [h._Open,h._High,h._Low,h._Close]
      hist_volumn.push
        x: strDate
        y: h._Volume

    # render candlestick chart
    candlestickChart = new CanvasJS.Chart "candlestickChartContainer",
      title:
        text: "Candle Stick Chart: " + templateData.symbol
      zoomEnabled: true
      backgroundColor: ""
      axisY:
        includeZero:false
        title: "Prices"
        prefix: " "
        suffix: " p"
        labelFontSize: 12
        valueFormatString: "0000"
      axisX:
        interval:2
        labelFontSize: 12
        intervalType: "month"
        valueFormatString: "MMM-YY"
        labelAngle: -45
      data: [
        {
          type: "candlestick"
          risingColor: "#EDCDFF"
          color: "#9A65AB"
          dataPoints: history
        }
      ]

    candlestickChart.render()

    # render volumn chart
    volumnChart = new CanvasJS.Chart "volumnChartContainer",
      zoomEnabled: true
      backgroundColor: ""
      axisY:
        includeZero:false
        title: "Volumn"
        labelFontSize: 12
        valueFormatString: "00.0E+0"
      axisX:
        interval:2
        intervalType: "month"
        valueFormatString: "MMM-YY"
        labelAngle: -45
        labelFontSize: 12
      data: [
        {
          dataPoints: hist_volumn
          color: "#EDCDFF"
        }
      ]

    volumnChart.render()

    console.log volumnChart
  )
  .fail(->
    console.log 'Faild to retrieve history'
  )
