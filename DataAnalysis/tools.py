import numpy as np
import math
import time
import datetime
import urllib2
from scipy import stats
from django.utils import timezone

def get_slope(values):
    v_max = np.max(values)
    v_min = np.min(values)
    n_value = len(values)


    slope, intercept, r_value, p_value, std_err = stats.linregress(np.linspace(v_min, v_max, n_value), values)

    if math.isnan(slope):
        slope = 0
    return slope

def get_stock_history(stock, period=30):
    dt = timezone.now()
    past = dt + datetime.timedelta(days=-period)
    return stock.stockhistory_set.filter(pub_date__gte=past).order_by('pub_date')


def safe_request(url):
    header = {'User-Agent': 'Mozilla/5.0'}

    html = ""
    retry = 1200
    while not html:
        try:
            html = urllib2.urlopen(
                urllib2.Request(
                    url, headers=header
                )
            )
        except Exception as e:
            print e
            print 'Retry in {} mins'.format(retry/60)
            html = ""
            time.sleep(retry)
            retry *= 2

    return html
