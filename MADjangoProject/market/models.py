from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

class Stock(models.Model):
    Symbol = models.CharField(max_length=20)
    Query = models.CharField(max_length=40, default='')
    Name = models.CharField(max_length=200, default='')
    Catagory = models.CharField(max_length=200, default='')
    Sector = models.CharField(max_length=200, default='')
    MarketCap = models.FloatField(default=0)
    Profit = models.FloatField(default=0)
    MPRatio = models.FloatField(default=0)
    PE = models.FloatField(default=0)
    EMS = models.FloatField(default=0)
    Bid = models.FloatField(default=0)
    Offer = models.FloatField(default=0)
    Spread = models.FloatField(default=0)
    Dividend = models.FloatField(default=0)
    NetDebt = models.FloatField(default=0)
    Liquidity = models.FloatField(default=0)
    DPRatio = models.FloatField(default=0)
    ProfitTrend = models.FloatField(default=0)
    DividendTrend = models.FloatField(default=0)
    DebtTrend = models.FloatField(default=0)
    Price = models.FloatField(default=0)
    update_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.Symbol

class StockHistory(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    Open = models.FloatField(default=0)
    Close = models.FloatField(default=0)
    High = models.FloatField(default=0)
    Low = models.FloatField(default=0)
    Volumn = models.FloatField(default=0)
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.stock.Symbol
