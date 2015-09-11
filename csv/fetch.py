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

# if __name__ == '__main__':

#     def fetchstore(symbol):
#         try:
#             info = json.dumps(get_info(symbol))
#             history = json.dumps(get_historical_info(symbol))

#             with open('db/{}.txt'.format(symbol),'w') as fi:
#                 fi.write(info)

#             with open('db/{}.csv'.format(symbol),'w') as fi:
#                 fi.write(history)

#         except:
#             print 'Failed with symbol:' + i


#     threads = []
#     open('symbols.txt', 'w').close()
#     for j in ['ftseallshare','ftseaimallshare']:
#         stocks = getlist(j)
#         with open('symbols.txt', 'a') as f:
#             for i in stocks:
#                 print 'Fetching Data: ' + i
#                 f.write('{}\n'.format(i))
#                 fetchstore(i)
#                 # t = threading.Thread(target=fetchstore, args=(i,))
#                 # threads.append(t)
#                 # t.start()

#         time.sleep(1800)

#     # for t in threads:
#         # t.join()

                
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
   
        with open('db/{}.json'.format(symbol),'w') as fi:
            fi.write(json.dumps(info))

    # Get Share History
    count = 0
    for share in FTSE['FTSEALL']+FTSE['FTSEAIM']:
        print 'Fetching history of ' + share['name']
        count += 1
        symbol = share['symbol']
        hist = get_historical_info(symbol,collection=stockDB)
        with open('db/{}.csv'.format(symbol),'w') as fi:
            fi.write(json.dumps(hist))
        if count % 500 == 0:
            time.sleep(600)
