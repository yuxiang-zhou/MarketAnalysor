import urllib2
import threading
from bs4 import BeautifulSoup
import re
import json
from django.utils import timezone
from tools import get_slope
from tools import safe_request
import itertools

query_url = 'http://www.londonstockexchange.com/exchange/prices/stocks/summary/fundamentals.html?fourWayKey={}'

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


def getLSEURLSymbol(symbol, collection=None):
    url = 'http://www.londonstockexchange.com/exchange/searchengine/search.html?q={}&page={}'

    new_query = ""
    for p in itertools.count(start=1):
        html = safe_request(url.format(symbol, p))
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table', class_='table_dati')
        if table and not new_query:
            for tr in table.find('tbody').find_all('tr'):
                [sSymbol, sLink, sType] = tr.find_all('td')[:3]
                type = sType.string.strip()
                if type != 'Stocks':
                    continue
                check = ''.join(map(lambda x: x if isinstance(x,str) else x.string, sSymbol.contents)).strip()
                if check == symbol.upper():
                    href = sLink.find('a')['href']
                    new_query = href.split('.html')[0].split('/')[-1]
                    if collection:
                        obj = collection.objects.get(Symbol=symbol)
                        obj.Query = new_query
                        obj.save()
                    break

        else:
            break

    return new_query


def getLSEInfo(query,symbol,collection=None):

    def valid_str(input_str):
        input_str = re.sub('[^0-9a-zA-Z]+', '', input_str)
        return input_str

    def valid_num(input_str):
        try:
            input_str = re.sub('[^0-9.-]+', '', input_str)

            if len(input_str) and input_str != '-':
                return float(input_str)
        except:
            pass
        return 0.0

    header = {'User-Agent': 'Mozilla/5.0'}

    info = {}

    querys = [
        query,
        getLSEURLSymbol(symbol, collection=collection)
    ]

    found = False
    for query in querys:
        try:
            html = safe_request(query_url.format(query))
            soup = BeautifulSoup(html, 'html.parser')
            tIncome,tBalance,tRatio,tCompany,tTrading = soup.find_all('table')
            found = True
            break
        except:
            continue

    if not found:
        print 'Data not Available'
        return info


    # Income Table
    detail = {}
    for tr in tIncome.find('tbody').find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) > 1:
            index = valid_str(tds[0].string)
            detail[index] = [valid_num(td.string) for td in tds[1:]]
    info['Income'] = detail

    # Balance Table
    detail = {}
    for tr in tBalance.find('tbody').find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) > 1:
            index = valid_str(tds[0].string)
            detail[index] = [valid_num(td.string) for td in tds[1:]]
    info['Balance'] = detail

    # Ratio Table
    detail = {}
    for tr in tRatio.find('tbody').find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) > 1:
            index = valid_str(tds[0].string)
            detail[index] = [valid_num(td.string) for td in tds[1:]]
    info['Ratio'] = detail

    # Company
    detail = {}
    for tr in tCompany.find('tbody').find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) > 1:
            index = valid_str(tds[0].string)
            detail[index] = valid_num(tds[-1].string) if 'Marketcap' in index else tds[-1].string
    info['Company'] = detail

    # Trading
    detail = {}
    for tr in tTrading.find('tbody').find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) > 1:
            index = valid_str(tds[0].string)
            detail[index] = valid_num(tds[-1].string) if 'Exchange' in index else tds[-1].string
    info['Trading'] = detail

    # Get Spread
    url = 'http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/summary/company-summary/{}.html'
    html = urllib2.urlopen(
        urllib2.Request(
            url.format(query),headers=header
        )
    )
    soup = BeautifulSoup(html, 'html.parser')
    try:
        tSummary = soup.find_all('table')[0]
    except:
        print 'Data not Available'
        return info

    detail = {}
    for tr in tSummary.find('tbody').find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) > 1:
            for index, value in zip(tds[0::2],tds[1::2]):
                index = valid_str(index.string)
                detail[index] = value.string if 'Var' in index or 'Last' in index or 'status' in index or 'Special' in index or index == '' else valid_num(value.string)
    info['Summary'] = detail

    stats = {}
    # DATA orgainising --------------------------
    stats['MarketCap'] = info['Company']['Marketcapinmillions']
    stats['Profit'] = info['Income']['ProfitBeforeTax'][-1]
    stats['MPRatio'] = stats['MarketCap'] / stats['Profit'] if stats['Profit'] > 0 else 999
    stats['PE'] = info['Ratio']['PERatioAdjusted'][-1]
    stats['EMS'] = info['Trading']['Exchangemarketsize']
    offer = info['Summary']['Offer']
    bid = info['Summary']['Bid']
    stats['Spread'] = 100 * (offer - bid) / bid if bid > 0 else 99
    stats['Dividend'] = info['Ratio']['DividendYield'][-1]
    stats['NetDebt'] = info['Balance']['TotalLiabilities'][-1]
    try:
        stats['Price'] = info['Summary']['PriceGBX']
    except:
        stats['Price'] = 0
        print 'Price is not GBP'
    stats['Bid'] = info['Summary']['Bid']
    stats['Offer'] = info['Summary']['Offer']
    stats['Liquidity'] = stats['EMS'] * stats['Price'] / 100.0
    stats['DPRatio'] = stats['NetDebt'] / stats['Profit'] * -1.0 if stats['Profit'] != 0 else 3
    # -------------------------------------------
    info['stats'] = stats

    if collection:
        obj, created = collection.objects.get_or_create(Symbol=symbol)
        obj.MarketCap = stats['MarketCap']
        obj.Profit = stats['Profit']
        obj.MPRatio = stats['MPRatio']
        obj.PE = stats['PE']
        obj.EMS = stats['EMS']
        obj.Bid = stats['Bid']
        obj.Offer = stats['Offer']
        obj.Spread = stats['Spread']
        obj.Price = stats['Price']
        obj.Dividend = stats['Dividend']
        obj.NetDebt = stats['NetDebt']
        obj.Liquidity = stats['Liquidity']
        obj.DPRatio = stats['DPRatio']
        obj.Sector = info['Trading']['FTSEsector']
        obj.Catagory = info['Trading']['FTSEindex']
        obj.ProfitTrend = get_slope(info['Income']['ProfitBeforeTax'])
        obj.DividendTrend = get_slope(info['Ratio']['DividendYield'])
        obj.DebtTrend = get_slope(info['Balance']['TotalLiabilities'])
        obj.pub_date = timezone.now()
        obj.save()

    return info


if __name__ == '__main__':
    # print getLSEURLSymbol('aaa')

    print json.dumps(getLSEInfo('GI000A0F6407GBGBXSTMM','888'))
