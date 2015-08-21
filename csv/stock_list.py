import urllib2
import threading
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


if __name__ == '__main__':
    open('symbols.txt', 'w').close()
    for j in ['ftseallshare','ftseaimallshare']:
        stocks = getlist(j)
        with open('symbols.txt', 'a') as f:
            for i in stocks:
                f.write('{}\n'.format(i))

        print j, len(stocks)