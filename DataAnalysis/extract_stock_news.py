import urllib2
import threading
from bs4 import BeautifulSoup
import re
import json
import datetime
import time
from django.utils import timezone
from tools import safe_request

url_base = 'http://www.londonstockexchange.com'
query_format = 'http://www.londonstockexchange.com/exchange/news/market-news/market-news-home.html?nameCodeText={0}&searchType=searchForNameCode&nameCode={0}&text=&rnsSubmitButton=Search&activatedFilters=true&newsSource=ALL&mostRead=&headlineCode=ONLY_EARNINGS_NEWS&headlineId=&ftseIndex=&sectorCode=&rbDate=released&preDate=LastMonth&newsPerPage=500'

def get_stock_news(symbol, collection=None):
    html = safe_request(query_format.format(symbol))
    soup = BeautifulSoup(html, 'html.parser')
    news_table = soup.find('table', class_='RNS_results_table')
    if news_table:
        for table in news_table.find_all('table'):
            firstrow, secondrow = table.find_all('tr')
            title = firstrow.find('span').string.strip() + ' - ' + firstrow.find('a').string.strip()
            url = url_base +  firstrow.find('a')['href'].strip().split(
                'openWin2(\''
            )[-1].split('.html')[0].strip() + '.html'
            date_str = secondrow.find('span').string.strip()
            date = timezone.datetime.strptime(date_str, '%H:%M %d-%b-%Y')

            obj, created = collection.objects.get_or_create(Symbol=symbol)
            obj_news, created = obj.stocknews_set.get_or_create(
                pub_date=date, url=url, title=title
            )
            if created:
                obj_news.save()


if __name__ == '__main__':
    print get_stock_news('HOME')
