import urllib2
import threading
from bs4 import BeautifulSoup
import re
import json
import datetime
from django.utils import timezone

def get_historical_info(symbol,collection=None):
    # Helper Function
    def float_parse(x):
        result = -1
        try:
            result = float(x)
        except:
            pass

        return result

    # Formating Query
    history_query = 'http://www.google.co.uk/finance/historical?q={}&startdate=Jan+1%2C+1990&enddate=Jan+1%2C+2100&num=30&output=csv'
    history_str=""

    # Download History Data
    try:
        history_str = urllib2.urlopen(history_query.format(symbol)).read()
        print 'Data Downloaded'
    except:
        try:
            history_str = urllib2.urlopen(history_query.format(symbol.replace('.', ''))).read()
        except:
            print "History not found or connection failed"

    # String Formating
    data = [i.split(',') for i in history_str.splitlines()]
    history = []
    if data:
        labels = data[0]
        data = data[1:]
        history = [[timezone.datetime.strptime(d[0], '%d-%b-%y')] + map(float_parse, d[1:]) for d in data]

        # Store to DB if exist
        if collection:
            for d in history:
                update_data = {}
                for l,p in zip(labels[1:],d[1:]):
                    update_data['_'+l.strip()] = p
                obj, created = collection.objects.get_or_create(Symbol=symbol)
                obj_hist, created = obj.stockhistory_set.get_or_create(pub_date=d[0])
                if not created:
                    break
                obj_hist.Open = update_data['_Open']
                obj_hist.Close = update_data['_Close']
                obj_hist.High = update_data['_High']
                obj_hist.Low = update_data['_Low']
                obj_hist.Volumn = update_data['_Volume']

                obj_hist.save()

            print 'Data Stored'



    return history

if __name__ == '__main__':
    symbol = 'III'
    data = get_historical_info(symbol)
    with open('{}.txt'.format(symbol), 'w') as f:
        f.write(data)
