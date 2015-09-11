Session.set 'basicFilter', true

Template.stocklist.helpers
  tableEntry: (index) ->
    BSF =
      'Trading.FTSEindex':
        $regex:
          ".*"+index+".*"

    if Session.get 'basicFilter'
      return StockDB.find(_.extend(BSF, BasicStockFilter))
    else
      return StockDB.find()

Template.stock_table.events
  'click #stockFilter': (e, t) ->
    Session.set 'basicFilter', e.target.checked