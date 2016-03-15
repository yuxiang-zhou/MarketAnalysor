import urllib2
import threading
from bs4 import BeautifulSoup
import re
import json
import numpy as np
import sys
import os
import django
import menpo.io as mio
from django.utils import timezone
import datetime

from stock_list import getlist, getLSEList
from extract_stock_info import get_info, getLSEInfo
from extract_stock_history import get_historical_info
from tools import get_stock_history
import time
from pymongo import MongoClient
import warnings
import exceptions
warnings.filterwarnings("ignore", category=exceptions.RuntimeWarning, module='django.db.backends.sqlite3.base', lineno=53)


def get_period_analysis(collection, period=30):

    gain_list = []
    if collection:
        for stock in collection.objects.all():
            hist = get_stock_history(stock, period=period)
            if hist:
                break_out = hist.last().Close - hist.first().Close
                break_out = np.divide(break_out , hist.first().Close)
                gain_list.append({
                    'stock':stock, 'break_out':break_out * 100
                })
    return gain_list

def data_slicing(collection, period=30, forward=30):
    gain_list = []
    if collection:
        for stock in collection.objects.all():
            ordered_hist = stock.stockhistory_set.order_by('pub_date')
            if ordered_hist:
                slices = []
                n_hist = ordered_hist.count()
                for i in range(n_hist + 1 - period - forward):
                    data = np.array([h.Close for h in ordered_hist[i:i+period]])
                    data = np.divide(data[1:] - data[:-1], data[0])
                    trend = np.array([h.Close for h in ordered_hist[i+period:i+period+forward]])
                    trend = np.divide(trend[-1] - trend[0], trend[0])

                    if not np.isinf(data).any() and not np.isinf(trend) and not np.isnan(data).any() and not np.isnan(trend):
                        slices.append({'data':data, 'trend':trend})

                gain_list.append({
                    stock.Symbol:slices
                })
    return gain_list

if __name__ == '__main__':
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../MADjangoProject'))
    if not path in sys.path:
        sys.path.insert(1, path)
    del path

    os.environ['DJANGO_SETTINGS_MODULE'] = 'MADjangoProject.settings'
    django.setup()

    from market.models import Stock, StockHistory
    import argparse

    # parse arguments

    parser = argparse.ArgumentParser(description='Stock Analysis')
    parser.add_argument('-p', dest='period_analysis', default=False, help='Period Analysis', action="store_true")
    parser.add_argument('-m', dest='ml_analysis', default=False, help='Machine Learning Prediction', action="store_true")
    args = parser.parse_args()

    if args.period_analysis:

        print 'Start Periodical Analysis'

        for result in get_period_analysis(Stock, period=7):
            stock = result['stock']
            stock.weekly_change = result['break_out']
            stock.save()

        for result in get_period_analysis(Stock, period=30):
            stock = result['stock']
            stock.monthly_change = result['break_out']
            stock.save()

        for result in get_period_analysis(Stock, period=90):
            stock = result['stock']
            stock.seasonally_change = result['break_out']
            stock.save()

        for result in get_period_analysis(Stock, period=180):
            stock = result['stock']
            stock.halfyearly_change = result['break_out']
            stock.save()

        for result in get_period_analysis(Stock, period=365):
            stock = result['stock']
            stock.yearly_change = result['break_out']
            stock.save()

        print 'Periodical Analysis Done'

    if args.ml_analysis:
        print 'Machine Learning Analysis Started Data Collection'
        store_path =  os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))

        for (pa, pb) in [(30,7),(90,30),(180,30),(180,90),(365,30),(365,90),(365,180)]:
            print 'Collecting Pattern: {} - {}'.format(pa,pb)
            slices = data_slicing(Stock, period=pa, forward=pb)
            mio.export_pickle(slices, '{}/{:03d}_{:03d}_slices.pkl'.format(store_path,pa,pb), overwrite=True)

        print 'Machine Learning Analysis Done'
