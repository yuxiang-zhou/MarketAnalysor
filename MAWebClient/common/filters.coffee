@BasicStockFilter = BasicStockFilter =
  'stats.MarketCap':
    $gte:
      49
    $lte:
      1000
  'stats.MPRatio':
    $lte:
      20
  'stats.Spread':
    $lte:
      3
  'stats.Liquidity':
    $gte:
      2000
  'stats.ProfitTrend':
    $gt:
      0
  'stats.DividentTrend':
    $gt:
      0
  'stats.NetDebtTrend':
    $gte:
      0
  # 'stats.PE':
  #   $lt:
  #     20
  #   $gt:
  #     10
