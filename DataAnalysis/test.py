import urllib2
import threading
from bs4 import BeautifulSoup
import re
import json
import sys
import os
import django

from stock_list import getlist, getLSEList
from extract_stock_info import get_info, getLSEInfo
from extract_stock_history import get_historical_info
from extract_sector_history import get_sector_history, get_sector_dict
from extract_stock_news import get_stock_news
from extract_NT_transactions import get_NT_transactions
import time
from pymongo import MongoClient
import warnings
import exceptions
warnings.filterwarnings("ignore", category=exceptions.RuntimeWarning, module='django.db.backends.sqlite3.base', lineno=53)

if __name__ == '__main__':
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../MADjangoProject'))
    if not path in sys.path:
        sys.path.insert(1, path)
    del path

    os.environ['DJANGO_SETTINGS_MODULE'] = 'MADjangoProject.settings'
    django.setup()

    from market.models import Stock, StockHistory, SectorHistory
    sec_dict = get_sector_dict()

    print 'Fethcing Indices...'
    ALL_Stocks = getLSEList(collection=Stock)

    def get_share_info():
        for share in ALL_Stocks:
            print 'Fetching info of ' + share['name']
            info = getLSEInfo(share['query'], share['symbol'],collection=Stock, sector_dict=sec_dict)


    import threading
    print 'Distributing Jobs ...'
    threads = []
    # callables = [get_nt]
    callables = [get_share_info]
    for f in callables:
        t = threading.Thread(target=f)
        t.setDaemon(True)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
