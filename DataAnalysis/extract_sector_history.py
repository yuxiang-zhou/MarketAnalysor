import urllib2
import threading
from bs4 import BeautifulSoup
import re
import json
import datetime
import time
from django.utils import timezone
from django.db.models import Avg

def get_sector_dict():
    sector_dict = {}
    mapping_query = 'https://www.google.co.uk/finance?q=FTSE+350+Index&restype=company&num=80'

    # Download History Data
    try:
        html = urllib2.urlopen(mapping_query).read()
        print 'Sector Mapping Downloaded'
    except Exception as e:
        print e

    # String Formating
    soup = BeautifulSoup(html, 'html.parser')

    for index in range(1,100):
        name = soup.find("a", {"id": "rc-{}".format(index)})
        query = soup.find("a", {"id": "rct-{}".format(index)})
        if not name:
            break
        else:
            sector_dict[name.string.replace('FTSE 350 Index - ', '')] = query.string

    return sector_dict


def calculate_sector_history(sector, collection=None, period=365):
    history = []
    dt = datetime.date.today()

    if collection:
        for i in range(period):

            past = dt + datetime.timedelta(days=-1)

            day_hists = collection.objects.filter(
                stock__Sector__contains=sector
            ).filter(
                pub_date__gte=past
            ).filter(pub_date__lt=dt)

            dt = past

            day_avg = day_hists.aggregate(
                Open=Avg('Open'),
                High=Avg('High'),
                Low=Avg('Low'),
                Close=Avg('Close'),
                Volumn=Avg('Volumn')
            )

            day_avg['pub_date'] = dt

            if day_avg['Close']:
                history.append(day_avg)

    return history

def get_sector_history(symbol,name,collection=None):
    # Helper Function
    def float_parse(x):
        result = -1
        try:
            result = float(x)
        except:
            pass

        return result

    # Formating Query
    history_query = 'http://real-chart.finance.yahoo.com/table.csv?s=%5E{}&d=1&e=25&f=2099&g=d&a=0&b=1&c=2000&ignore=.csv'
    history_str=""
    history = []
    # Download History Data
    try:
        history_str = urllib2.urlopen(history_query.format(symbol)).read()
        print 'Downloading {} from Yahoo'.format(name)

        # String Formating
        data = [i.split(',') for i in history_str.splitlines()]

        if data:
            hasdata = True
            labels = data[0]
            data = data[1:]
            history = [[timezone.datetime.strptime(d[0], '%Y-%m-%d')] + map(float_parse, d[1:]) for d in data]
    except Exception as e:
        print e
        return
        try:
            print 'Downloading {} from Google'.format(name)

            def find_between( s, first, last ):
                try:
                    start = s.index( first ) + len( first )
                    end = s.index( last, start )
                    return s[start:end]
                except ValueError:
                    return ""

            labels = ['Date','Open','High','Low','Close','Volume']
            page_size = 200
            history_query = 'https://www.google.co.uk/finance/historical?q=INDEXFTSE:{}&startdate=Jan%201%2C%202000&enddate=Feb%2099%2C%202016&num='+ str(page_size) +'&start={}'

            index = 0
            done = False
            while True:
                hist_temp = []

                history_str = ''
                retry_gap = 1800
                while not history_str:
                    try:
                        history_str = urllib2.urlopen(history_query.format(symbol, index)).read()
                    except Exception as e:
                        history_str = ''
                        print 'Failed to get data, retry in {:02d} mins'.format(retry_gap / 60)
                        time.sleep(retry_gap)
                        retry_gap *= 2
                rows = find_between(history_str, '<table class="gf-table historical_price">','</table>')
                rows = rows.split('<tr>')
                for r in rows[1:]:
                    r = r.split('<td  class="rgt">')
                    r = map(lambda x:x.replace('\n','').replace(',',''), r)
                    r[0] = r[0].replace('<td  class="lm">','')
                    r[-1] = r[-1].split('<')[0]
                    hist_temp.append([timezone.datetime.strptime(r[0], '%b %d %Y')] + map(float_parse, r[1:] + [0]))

                # print rows

                index += page_size

                for hist in hist_temp:
                    if collection.objects.filter(Sector=name,Symbol=symbol,pub_date=hist[0]).exists():
                        done = True
                        break

                history += hist_temp
                # if len(hist_temp) < page_size or done:
                #     break

            hasdata = True

            print 'Data Downloaded'

        except Exception as e:
            print e
            return



    if hasdata and collection:
        # Store to DB if exist
        for d in history:
            update_data = {}
            for l,p in zip(labels[1:],d[1:]):
                update_data['_'+l.strip()] = p
            obj, created = collection.objects.get_or_create(Sector=name,Symbol=symbol,pub_date=d[0])
            if not created:
                break
            obj.Open = update_data['_Open']
            obj.Close = update_data['_Close']
            obj.High = update_data['_High']
            obj.Low = update_data['_Low']
            obj.Volumn = update_data['_Volume']

            obj.save()

        print '{} Data Stored'.format(len(history))



    return history

if __name__ == '__main__':
    dict = {}
    for k in dict.keys():
        get_sector_history(dict[k], k)
        break
