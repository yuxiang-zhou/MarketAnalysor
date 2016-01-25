import urllib2
import threading
from bs4 import BeautifulSoup
import re
import json
import sys

from stock_list import getlist, getLSEList
from extract_stock_info import get_info, getLSEInfo
from extract_stock_history import get_historical_info
import time
from pymongo import MongoClient


if __name__ == '__main__':
    # Connect MongoDB
    host = 'localhost'
    port = 27017
    if len(sys.argv) > 1:
        host = sys.argv[1]
    if len(sys.argv) > 2:
        port = int(sys.argv[2])

    try:
        print 'Try connecting db...'
        client = MongoClient("mongodb://"+host, port)
        print 'Done.'
        db = client.meteor
        stockDB = db.stock
        stockDBHist = db.stockhist
    except:
        print "Unexpected error:", sys.exc_info()[0]
        exit()




    print 'Fethcing Indices...'
    FTSE = getLSEList(collection=stockDB)

    # Get Share Info
    for share in FTSE['FTSEALL']+FTSE['FTSEAIM']:
        print 'Fetching info of ' + share['name']
        info = getLSEInfo(share['query'],collection=stockDB)
        symbol = share['symbol']


    # Get Share History
    count = 0
    for share in FTSE['FTSEALL']+FTSE['FTSEAIM']:
        print 'Fetching history of ' + share['name']
        count += 1
        symbol = share['symbol']
        hist = get_historical_info(symbol,collection=stockDBHist)
        # with open('db/{}.csv'.format(symbol),'w') as fi:
        #     fi.write(json.dumps(hist))
