import urllib2
import threading
from bs4 import BeautifulSoup
import re
import json

def get_info(symbol):
    info_query = 'https://www.google.co.uk/finance?q={}'
    filtering_str = 'google.finance.data'

    html = urllib2.urlopen(info_query.format(symbol)).read()
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find('div', class_='g-wrap')
    news = soup.find_all('script')
    
    # parse news
    newsdata=""
    for script in news:
        if script.string and filtering_str in script.string:
            scriptdata = script.string.splitlines()
            for l in scriptdata:
                if l.startswith(filtering_str + ' ='):
                    newsdata = l[len(filtering_str)+3:-1]
                    break
            break

    newsdata = re.sub(r'\{(\w+):',r'{"\1":',newsdata)
    newsdata = re.sub(r',(\w+):',r',"\1":',newsdata)
    info = json.loads(newsdata)['company']

    # parse info
    marketdata = {}
    market_data_div = content.find('div', id='market-data-div')
    marketdata['price'] = "".join([sp.string for sp in market_data_div.find('span', class_='pr').find_all('span')])
    
    pricechange = content.find('div', class_='id-price-change').find('span')
    marketdata['pricechange'], marketdata['pricechangepercent'] = [sp.string for sp in pricechange.find_all('span')]

    for tr in content.find('div', class_='snap-panel').find_all('tr'):
        title, value = [td.get_text() for td in tr.find_all('td')]
        if not title:
            title = 'Currency'

        marketdata[title.strip()] = value.strip().replace("*","")
    info['marketdata'] = marketdata

    return info


def getLSEInfo(query,collection=None):

    def valid_str(input_str):
        return input_str.strip().replace('.','')

    header = {'User-Agent': 'Mozilla/5.0'}

    info = {}

    url = 'http://www.londonstockexchange.com/exchange/prices/stocks/summary/fundamentals.html?fourWayKey={}'
    html = urllib2.urlopen(
        urllib2.Request(
            url.format(query),headers=header
        )
    )
    soup = BeautifulSoup(html, 'html.parser')
    try:
        tIncome,tBalance,tRatio,tCompany,tTrading = soup.find_all('table')
    except:
        print 'Data not Available'
        return info


    # Income Table
    detail = {}
    for tr in tIncome.find('tbody').find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) > 1:
            index = valid_str(tds[0].string)
            detail[index] = [td.string.strip() for td in tds[1:]]
    info['Income'] = detail

    # Balance Table
    detail = {}
    for tr in tBalance.find('tbody').find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) > 1:
            index = valid_str(tds[0].string)
            detail[index] = [td.string.strip() for td in tds[1:]]
    info['Balance'] = detail

    # Ratio Table
    detail = {}
    for tr in tRatio.find('tbody').find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) > 1:
            index = valid_str(tds[0].string)
            detail[index] = [td.string.strip() for td in tds[1:]]
    info['Ratio'] = detail

    # Company
    detail = {}
    for tr in tCompany.find('tbody').find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) > 1:
            index = valid_str(tds[0].string)
            detail[index] = tds[-1].string.strip()
    info['Company'] = detail

    # Trading
    detail = {}
    for tr in tTrading.find('tbody').find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) > 1:
            index = valid_str(tds[0].string)
            detail[index] = tds[-1].string.strip()
    info['Trading'] = detail

    if collection:
        collection.update({
            'query':query
        },{'$set' : info})

    return info


if __name__ == '__main__':
    print json.dumps(getLSEInfo('GB00BJTNFH41GBGBXSTMM'))
