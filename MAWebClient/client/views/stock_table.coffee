Session.set 'basicFilter', true
# Session.set 'IndexElements', [
#     {label:'FTSE All-Share',path:'#FTSEAS'},
#     {label:'FTSE AIM All-Share',path:'#FTSEAAS'}
#   ]

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

  tableHasRecord: (index) ->
    BSF =
      'Trading.FTSEindex':
        $regex:
          ".*"+index+".*"

    if Session.get 'basicFilter'
      return StockDB.findOne(_.extend(BSF, BasicStockFilter))
    else
      return StockDB.findOne()

Template.stock_table.helpers
  basicfilter: ->
    return Session.get 'basicFilter'

Template.stock_table.events
  'click #stockFilter': (e, t) ->
    Session.set 'basicFilter', e.target.checked

Template.stockEntry.events
  'click .clickable-row': (e,t) ->
    symbol=Template.instance().data.symbol
    Router.go('/stockdetail/'+symbol)
