import urllib2
import threading
from bs4 import BeautifulSoup
import re
import json
import sys
import os
import django
import datetime
from django.utils import timezone

from stock_list import getlist, getLSEList
from extract_stock_info import get_info, getLSEInfo
from extract_stock_history import get_historical_info
from extract_sector_history import get_sector_history, get_sector_dict, calculate_sector_history
from extract_stock_news import get_stock_news
from extract_NT_transactions import get_NT_transactions
import time
from pymongo import MongoClient
import warnings
import exceptions
import pickle

warnings.filterwarnings("ignore", category=exceptions.RuntimeWarning, module='django.db.backends.sqlite3.base', lineno=53)

if __name__ == '__main__':
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../MADjangoProject'))
    if not path in sys.path:
        sys.path.insert(1, path)
    del path

    os.environ['DJANGO_SETTINGS_MODULE'] = 'MADjangoProject.settings'
    django.setup()

    from market.models import Stock, StockHistory, SectorHistory, StockNT
    import argparse

    # parse arguments

    parser = argparse.ArgumentParser(description='Stock Fetching')
    parser.add_argument('-a', dest='stock_list_update', default=False, help='Stock List Update', action="store_true")
    parser.add_argument('-i', dest='stock_info_list', default=False, help='Stock Infomation List', action="store_true")
    parser.add_argument('-l', dest='stock_history_list', default=False, help='Stock History List', action="store_true")
    parser.add_argument('-n', dest='stock_news_list', default=False, help='Stock News List', action="store_true")
    parser.add_argument('-t', dest='NT_list', default=False, help='Naked Trader List', action="store_true")
    parser.add_argument('-s', dest='sector_history_list', default=False, help='Sector History List', action="store_true")
    args = parser.parse_args()

    sectors = [s.Sector for s in Stock.objects.distinct('Sector') if s.Sector]

    print 'Fethcing Indices...'

    dt = timezone.now()
    fn = '{:04d}{:02d}{:02d}.pkl'.format(dt.year,dt.month,dt.day)

    ALL_Stocks = []
    for s in Stock.objects.all():
        ALL_Stocks.append({
            "symbol": s.Symbol,
            "name": s.Name,
            "query": s.Query,
        })

    def get_share_list():
        getLSEList(collection=Stock)


    def get_share_info():
        for share in ALL_Stocks:
            print 'Fetching info of ' + share['name']
            info = getLSEInfo(share['query'], share['symbol'],collection=Stock)

    def get_share_hist():
        count = 0
        for share in ALL_Stocks:
            print 'Fetching history of ' + share['name']
            count += 1
            symbol = share['symbol']
            hist = get_historical_info(symbol,collection=Stock)

    def calculate_sector_hist():
        for sector in sectors:
            print 'Calculating sector {}'.format(sector)
            hist = calculate_sector_history(
                sector, collection=StockHistory
            )

            for h in hist:
                obj, created = SectorHistory.objects.get_or_create(
                    Sector=sector, pub_date=h['pub_date']
                )

                if created:
                    obj.Symbol = sector
                    obj.Open = h['Open']
                    obj.High = h['High']
                    obj.Low = h['Low']
                    obj.Close = h['Close']
                    obj.Volumn = h['Volumn']
                    obj.save()




    def get_sector_hist():
        sec_dictionary = {'FTSE':'FTSE', 'FTAI':'FTAI'}
        for sector in sec_dictionary.keys():
            print 'Fethcing {} Sector Histories'.format(sector)
            get_sector_history(
                sec_dictionary[sector],
                sector,
                collection=SectorHistory
            )

    def get_stock_news_list():
        for share in ALL_Stocks:
            print 'Fethcing News of ' + share['name']
            get_stock_news(share['symbol'], share['query'], collection=Stock)

    def get_nt():
        print 'Fethcing NT Suggestions'
        # StockNT.objects.all().delete()
        get_NT_transactions(collection=Stock)

    import threading
    print 'Distributing Jobs ...'

    threads = []
    callables = []
    if args.stock_list_update:
        callables.append(get_share_list)
    if args.stock_info_list:
        callables.append(get_share_info)
    if args.stock_history_list:
        callables.append(get_share_hist)
        callables.append(get_sector_hist)
    if args.stock_news_list:
        callables.append(get_stock_news_list)
    if args.NT_list:
        callables.append(get_nt)
    if args.sector_history_list:
        callables.append(calculate_sector_hist)


    for f in callables:
        t = threading.Thread(target=f)
        t.setDaemon(True)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
