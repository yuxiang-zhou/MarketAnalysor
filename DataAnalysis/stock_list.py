import urllib2
import threading
import json
import time
from django.utils import timezone
from bs4 import BeautifulSoup
from tools import safe_request

# stock list
def getlist(stock):
    stocks = []
    stock_list_query = 'http://shareprices.com/{}'

    html = urllib2.urlopen(stock_list_query.format(stock)).read()

    soup = BeautifulSoup(html, 'html.parser')
    for i in soup.find_all('tr', class_='tables1'):
        stocks.append(i.find('td').string)

    for i in soup.find_all('tr', class_='tables2'):
        stocks.append(i.find('td').string)

    return stocks


def getLSEList(collection=None):

    FTSE_ALL = 'http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/summary/summary-indices-constituents.html?index=ASX&page={}'
    FTSE_AIM = 'http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/summary/summary-indices-constituents.html?index=AXX&page={}'

    ALL_Share = 'http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/prices-search/stock-prices-search.html?nameCode=&page={}'

    stock = []

    def get(url):
        lists = []
        n_pages = 1
        index = 0

        while index < n_pages:
            index += 1
            html = safe_request(url.format(index))
            soup = BeautifulSoup(html, 'html.parser')

            # get n_pages
            if n_pages == 1:
                n_pages = int(
                    soup.find('div', class_='paging').find(
                        'p'
                    ).string.split('of')[-1].strip()
                )

            print 'Fetching page {} of {}'.format(index, n_pages)

            # parse list
            for tr in soup.find('tbody').find_all('tr'):
                tds = tr.find_all('td')
                #construct data
                info = {}
                info['symbol'] = tds[0].string.strip()
                a = tds[1].find('a')
                info['name'] = a.string.strip()
                info['query'] = a.get('href').strip().split(
                    '/'
                )[-1].split('?')[0][:-5]

                lists.append(info)

                if collection:
                    obj, created = collection.objects.get_or_create(Symbol=info['symbol'])
                    obj.Query = info['query']
                    obj.Name = info['name']
                    obj.pub_date = timezone.now()
                    obj.save()

        return lists

    # for url,name in zip([FTSE_ALL, FTSE_AIM],['FTSEALL','FTSEAIM']):
    #     try:
    #         stock[name] = get(url)
    #     except:
    #         print 'Get list {} failed'.format(name)

    stock = get(FTSE_ALL) + get(FTSE_AIM)

    return stock



# if __name__ == '__main__':
#     open('symbols.txt', 'w').close()
#     for j in ['ftseallshare','ftseaimallshare']:
#         stocks = getlist(j)
#         with open('symbols.txt', 'a') as f:
#             for i in stocks:
#                 f.write('{}\n'.format(i))

#         print j, len(stocks)

if __name__ == '__main__':
    print json.dumps(getLSEList())
