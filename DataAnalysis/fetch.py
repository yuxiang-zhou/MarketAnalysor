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

    from market.models import Stock, StockHistory

    # Connect MongoDB
    # host = 'localhost'
    # port = 27017
    # if len(sys.argv) > 1:
    #     host = sys.argv[1]
    # if len(sys.argv) > 2:
    #     port = int(sys.argv[2])
    #
    # try:
    #     print 'Try connecting db...'
    #     client = MongoClient("mongodb://"+host, port)
    #     print 'Done.'
    #     db = client.meteor
    #     stockDB = db.stock
    #     stockDBHist = db.stockhist
    # except:
    #     print "Unexpected error:", sys.exc_info()[0]
    #     exit()
    #
    #
    #

    print 'Fethcing Indices...'
    FTSE = getLSEList(collection=Stock)
    #
    # Get Share Info
    for share in FTSE['FTSEALL']+FTSE['FTSEAIM']:
        print 'Fetching info of ' + share['name']
        info = getLSEInfo(share['query'],collection=Stock)
        symbol = share['symbol']


    # Get Share History
    count = 0
    for share in FTSE['FTSEALL']+FTSE['FTSEAIM']:
        print 'Fetching history of ' + share['name']
        count += 1
        symbol = share['symbol']
        hist = get_historical_info(symbol,collection=Stock)
        # with open('db/{}.csv'.format(symbol),'w') as fi:
        #     fi.write(json.dumps(hist))
