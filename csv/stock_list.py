import urllib2
import threading
import json
from bs4 import BeautifulSoup

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

    stock = {}

    def get(url):
        header = {'User-Agent': 'Mozilla/5.0'}

        lists = []
        n_pages = 1
        index = 0

        while index < n_pages:
            index += 1

            html = urllib2.urlopen(
                urllib2.Request(
                    url.format(index),headers=header
                )
            )
            soup = BeautifulSoup(html, 'html.parser')

            # get n_pages
            if n_pages == 1:
                n_pages = int(
                    soup.find('div', class_='paging').find(
                        'p'
                    ).string.split('of')[-1].strip()
                )

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
                )[-1][:-5]

                lists.append(info)

                if collection:
                    collection.update({
                        'symbol':info['symbol']
                    },{'$set' : info},upsert=True)

        return lists

    for url,name in zip([FTSE_ALL, FTSE_AIM],['FTSEALL','FTSEAIM']):
        stock[name] = get(url)

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
