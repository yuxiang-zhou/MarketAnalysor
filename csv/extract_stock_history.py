import urllib2
import threading
from bs4 import BeautifulSoup
import re
import json

def get_historical_info(symbol,collection=None):
    history_query = 'http://www.google.co.uk/finance/historical?q={}&startdate=Jan+1%2C+1990&enddate=Jan+1%2C+2100&num=30&output=csv'
    history=""

    try:
        history = urllib2.urlopen(history_query.format(symbol)).read()
    except:
        try:
            history = urllib2.urlopen(history_query.format(symbol.replace('.', ''))).read()
        except:
            print "History not found or connection failed"


    if collection:
        collection.update({
            'symbol':symbol
        },{'$set' : {'history':history}})

    return history

if __name__ == '__main__':
    symbol = 'III'
    data = get_historical_info(symbol)
    with open('{}.txt'.format(symbol), 'w') as f:
        f.write(data)

