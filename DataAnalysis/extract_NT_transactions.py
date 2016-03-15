import urllib2
import threading
from bs4 import BeautifulSoup
import re
import json
import datetime
import time
from django.utils import timezone

query_format = 'http://nakedtrader.co.uk/'
header = {
    'User-Agent': 'Mozilla/5.0',
    'Cookie': 'nt=1'
}

def get_NT_transactions(collection=None):
    def safe_float(a):
        ret = 0
        try:
            ret = float(a)
        except:
            pass
        return ret

    def safe_date(d):
        try:
            return timezone.datetime.strptime(d, '%d/%m/%Y')
        except:
            return timezone.datetime.strptime('01/01/1970', '%d/%m/%Y')

    html = urllib2.urlopen(
        urllib2.Request(query_format,headers=header)
    )
    soup = BeautifulSoup(html, 'html.parser')
    share_table, spread_long, spread_short = soup.find_all('table', class_='trades')

    for tr in share_table.find_all('tr')[1:]:
        _,symbol,qty,price,target,stop,buy_date,sell,sell_date,pl = [td.string for td in tr.find_all('td')]

        if collection:
            stock = collection.objects.filter(Symbol=symbol)
            if stock:
                obj = stock[0]
                nt, created = obj.stocknt_set.get_or_create(
                    qty=safe_float(qty),price=safe_float(price),
                    buy_date=safe_date(buy_date)
                )
                if not created:
                    break
                nt.sell=safe_float(sell)
                nt.sell_date=safe_date(sell_date)
                nt.pl=safe_float(pl)
                nt.target=safe_float(target)
                nt.stop=safe_float(stop)
                nt.save()

if __name__ == '__main__':
    print get_NT_transactions()
