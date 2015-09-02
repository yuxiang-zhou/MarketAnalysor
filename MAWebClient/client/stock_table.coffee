Template.stocklist.helpers
  tableEntry: (index) ->
    BSF = BasicStockFilter
    BSF['Trading.FTSEindex'] =
      $regex:
        ".*"+index+".*"

    console.log BasicStockFilter
    return StockDB.find(BasicStockFilter)

# Template.stock_table.events
#   'click #stockFilter': () ->
#     console.log this