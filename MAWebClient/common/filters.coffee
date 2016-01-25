@BasicStockFilter = BasicStockFilter =
  'stats.MarketCap':
    $gt:
      49
    $lt:
      1000
  'stats.MPRatio':
    $lt:
      20
  'stats.Spread':
    $lt:
      3
  'stats.Liquidity':
    $gt:
      2000
  # 'stats.PE':
  #   $lt:
  #     20
  #   $gt:
  #     10
