fieldNoHistory = {
  'fields': {
    'symbol': 1,
    'name': 1,
    'query': 1,
    'stats': 1,
    'Company': 1,
    'Trading.FTSEindex': 1
  }
}


Meteor.publish "stocksFTSE", ->
  return StockDB.find({"Trading.FTSEindex": {"$regex":".*FTSE All-Share.*"}}, fieldNoHistory)

Meteor.publish "stocksFTSEAIM", ->
  return StockDB.find({"Trading.FTSEindex": {"$regex":".*AIM.*"}}, fieldNoHistory)

Meteor.publish "stocksall", ->
  return StockDB.find({}, fieldNoHistory)

  # MarketCap: ->
  #   mc = @Company.Marketcapinmillions
  #   return '£ '+mc+''
  # Profit: ->
  #   return @Income.ProfitBeforeTax[@Income.ProfitBeforeTax.length - 1]
  # MPRatio: ->
  #   mc = @Company.Marketcapinmillions
  #   profit = @Income.ProfitBeforeTax[@Income.ProfitBeforeTax.length - 1]
  #   return  (mc / profit).toFixed(2)
  # PE: ->
  #   return @Ratio.PERatioAdjusted[@Ratio.PERatioAdjusted.length-1]
  # EMS: ->
  #   return @Trading.Exchangemarketsize
  # Spread: ->
  #   offer = @Summary.Offer
  #   bid = @Summary.Bid
  #   spread = 100 * (offer - bid) / bid
  #   return bid + ' ~ '+offer+' ('+spread.toFixed(2)+'%)'
  # Dividend: ->
  #   return @Ratio.DividendYield[@Ratio.DividendYield.length-1]
  # NetDebt: ->
  #   return @Balance.Borrowings[@Balance.Borrowings.length-1]
