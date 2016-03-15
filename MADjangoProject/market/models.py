from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

class Stock(models.Model):
    # Basic Fields
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
    pub_date = models.DateTimeField(default=timezone.now)
    # Analysis Fields
    weekly_change = models.FloatField(default=0)
    monthly_change = models.FloatField(default=0)
    seasonally_change = models.FloatField(default=0)
    halfyearly_change = models.FloatField(default=0)
    yearly_change = models.FloatField(default=0)

    def __str__(self):
        return '{}, {}, {}, ({}, {})'.format(
            self.Symbol,
            self.Name,
            self.MarketCap,
            self.Catagory,
            self.pub_date
        )

class StockNT(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    qty = models.FloatField(default=0)
    price = models.FloatField(default=0)
    target = models.FloatField(default=0)
    stop = models.FloatField(default=0)
    sell = models.FloatField(default=0)
    pl = models.FloatField(default=0)
    buy_date = models.DateTimeField(default=timezone.now)
    sell_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.stock.Symbol

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


class StockNews(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, default='')
    url = models.CharField(max_length=512, default='')
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.stock.Symbol


class SectorHistory(models.Model):
    Sector = models.CharField(max_length=100, default='')
    Symbol = models.CharField(max_length=20, default='')
    Open = models.FloatField(default=0)
    Close = models.FloatField(default=0)
    High = models.FloatField(default=0)
    Low = models.FloatField(default=0)
    Volumn = models.FloatField(default=0)
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{} ({})'.format(self.Sector, self.pub_date)


class StockSelection(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.CharField(max_length=500, default='')
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.stock.Symbol

class StockPurchased(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.FloatField()
    target = models.FloatField(default=-1)
    stop = models.FloatField(default=-1)
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.stock.Symbol

class StockSold(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.FloatField()
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.stock.Symbol
