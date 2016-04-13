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
querys = [
    'http://www.londonstockexchange.com/exchange/prices-and-markets/rns/company-news.html?tidm={}&isin={}&newsType=',
    'http://www.londonstockexchange.com/exchange/news/alliance-news/company-news.html?tidm={}'
]

def get_stock_news(symbol, query, collection=None):
    for query_format in querys:
        html = safe_request(query_format.format(symbol, query.split('GBGB')[0]))
        soup = BeautifulSoup(html, 'html.parser')

        for news in soup.find_all('li', class_='newsContainer'):
            info = news.find('a')
            title = info.string.strip()
            url = url_base + info['href'].strip().split('.html')[0].strip().split("openWin2('")[-1] + '.html'
            date_str = news.find('span', class_='hour').string.strip()
            if len(date_str) <=5:
                date_str = timezone.datetime.now().strftime('%d %b %Y') + ' ' + date_str
            date = timezone.datetime.strptime(date_str, '%d %b %Y %H:%M')

            if collection:
                obj, created = collection.objects.get_or_create(Symbol=symbol)
                try:
                    obj_news, created = obj.stocknews_set.get_or_create(
                        pub_date=date, url=url, title=title
                    )
                    if created:
                        obj_news.save()
                except:
                    pass


if __name__ == '__main__':
    get_stock_news('JRP','GB00BCRX1J15GBGBXSTMM')
