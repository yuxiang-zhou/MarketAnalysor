Meteor.publish "stocksFTSE", ->
  return StockDB.find({"Trading.FTSEindex": {"$regex":".*FTSE.*"}})

Meteor.publish "stocksall", ->
  return StockDB.find()

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