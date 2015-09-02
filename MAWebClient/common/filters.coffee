@BasicStockFilter = BasicStockFilter =  
  'stats.MarketCap':
    $gt:
      49
    $lt:
      1000
  'stats.MPRatio':
    $lt:
      15
  'stats.PE':
    $lt:
      20
    $gt:
      10
  'stats.Spread':
    $lt:
      3