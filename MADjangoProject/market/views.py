from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.core import serializers
from django.utils import timezone
from django.contrib.auth import authenticate, login

import datetime
import urllib
import json

from .models import Stock, StockHistory, StockSelection, SectorHistory, StockNews, StockNT
from django.contrib.auth.models import User
from django.db.models import Q

sector_names = [s.Sector for s in Stock.objects.distinct('Sector') if s.Sector]

def navRoutes():
    return [{
        'path':reverse('market:index'),
        'isActive':False,
        'icon':'fa-home',
        'label':'Summary',
        'children': []
    },{
        'path':reverse('market:news'),
        'isActive':False,
        'icon':'fa-newspaper-o',
        'label':'Latest News',
        'children': []
    },{
        'path':reverse('market:sectors'),
        'isActive':False,
        'icon':'fa-area-chart',
        'label':'Sectors',
        'children': []
    },{
        'path':reverse('market:account'),
        'isActive':False,
        'icon':'fa-star',
        'label':'Favourite',
        'children': []
    },{
        'path':reverse('market:list'),
        'isActive':False,
        'icon':'fa-table',
        'label':'Stock Table',
        'children': [{
            'path':reverse('market:clist', kwargs={'catagory': 'ftse'}),
            'isActive':False,
            'icon':'fa-table',
            'label':'FTSE ALL',
            'children': []
        },{
            'path':reverse('market:clist', kwargs={'catagory': 'ftseaim'}),
            'isActive':False,
            'icon':'fa-table',
            'label':'FTSE AIM ALL',
            'children': []
        }]
    }]

# helper functions
def common_filter(objects, mcl=49, mch=4000, mp=20, spread=3, liq=2000, dp=3, trend=True, update_date=None):
    query =  objects.filter(MarketCap__gte=mcl).filter(MarketCap__lte=mch).filter(MPRatio__lte=mp).filter(Spread__lte=spread).filter(Liquidity__gte=liq).filter(DPRatio__lte=dp)

    if update_date:
        query = query.filter(pub_date__gte=update_date)

    if trend:
        query = query.filter(ProfitTrend__gte=-0.3).filter(DividendTrend__gte=-0.3).filter(DebtTrend__gte=-0.3)
    return query


def addCORSHeaders(theHttpResponse):
    theHttpResponse['Access-Control-Allow-Origin'] = '*'
    theHttpResponse['Access-Control-Max-Age'] = '120'
    theHttpResponse['Access-Control-Allow-Credentials'] = 'true'
    theHttpResponse['Access-Control-Allow-Methods'] = 'HEAD, GET, OPTIONS, POST, DELETE'
    theHttpResponse['Access-Control-Allow-Headers'] = 'origin, content-type, accept, x-requested-with, Authorization'
    return theHttpResponse


# api views
def history(request, symbol):
    return addCORSHeaders(HttpResponse(
        serializers.serialize(
            'json', Stock.objects.get(
                Symbol=symbol
            ).stockhistory_set.all().order_by('-pub_date')[:550]
        )
    ))


def historysector(request, sector):
    return addCORSHeaders(HttpResponse(
        serializers.serialize(
            'json', SectorHistory.objects.filter(
                Sector__contains=sector.replace('&amp;','&')
            ).order_by('-pub_date')[:550]
        )
    ))


def search(request, query):
    query = query.upper()
    context = Stock.objects.filter(
        Q(Symbol__contains=query) | Q(Name__contains=query)
    )

    return addCORSHeaders(
        HttpResponse(serializers.serialize('json', context))
    )


def list(request, indices):

    dt = timezone.now()
    past = dt + datetime.timedelta(days=-2)

    if indices == 'ftse':
        indices = 'FTSE All-Share'
    elif indices == 'ftai':
        indices = 'FTSE AIM All-Share'
    else:
        indices = ''

    context = common_filter(
        Stock.objects.filter(Catagory__contains=indices),
        update_date=past
    )

    return addCORSHeaders(
        HttpResponse(serializers.serialize('json', context))
    )


def news(request, symbol):

    dt = timezone.now()
    recent = dt + datetime.timedelta(days=-2)
    past = dt + datetime.timedelta(days=-365)

    def parseNews(data):
        return [
            {
                'title': news.title,
                'symbol': news.stock.Symbol,
                'pub_date': news.pub_date.strftime("%d-%b-%Y %H:%M"),
                'url': news.url
            } for news in data
        ]

    if(symbol == 'all'):
        context = parseNews(StockNews.objects.filter(
                pub_date__gte=recent
            ).order_by('-pub_date')[:800]
        )
    else:
        context = parseNews(StockNews.objects.filter(
                pub_date__gte=past, stock__Symbol=symbol
            ).order_by('-pub_date')
        )

    return addCORSHeaders(
        HttpResponse(json.dumps(context))
    )


def sectorlist(request):

    return addCORSHeaders(
        HttpResponse(json.dumps(sector_names))
    )


def detail(request, symbol):

    context = get_object_or_404(
        Stock.objects, Symbol=symbol.upper()
    )

    return addCORSHeaders(
        HttpResponse(serializers.serialize('json', [context]))
    )


def favlist(request, username):

    context = [sel.stock for sel in StockSelection.objects.filter(user__username=username)]

    return addCORSHeaders(
        HttpResponse(serializers.serialize('json', context))
    )


def favnews(request, username):

    favstocks = [
        sel.stock for sel in StockSelection.objects.filter(
            user__username=username
        )
    ]

    context = []
    dt = timezone.now()
    past = dt + datetime.timedelta(days=-3)
    for stock in favstocks:
        context += [
            {
                'title': news.title,
                'symbol': news.stock.Symbol,
                'pub_date': news.pub_date.strftime("%d-%b-%Y %H:%M"),
                'url': news.url
            } for news in StockNews.objects.filter(stock=stock, pub_date__gte=past).order_by('-pub_date')
        ]

    return addCORSHeaders(
        HttpResponse(json.dumps(context))
    )

def favlike(request, username, symbol):

    user = User.objects.get(username=username)
    stock = Stock.objects.get(Symbol=symbol)
    if(not StockSelection.objects.filter(user__username=username, stock__Symbol=symbol).exists()):
        selection = StockSelection(user=user, stock=stock)
        selection.save()

    return addCORSHeaders(
        HttpResponse(json.dumps({"success":True}))
    )

def favdislike(request, username, symbol):

    StockSelection.objects.filter(user__username=username, stock__Symbol=symbol).delete()

    return addCORSHeaders(
        HttpResponse(json.dumps({"success":True}))
    )

def isfav(request, username, symbol):

    result = StockSelection.objects.filter(user__username=username, stock__Symbol=symbol).exists()

    return addCORSHeaders(
        HttpResponse(json.dumps({"success":True, "result":result}))
    )


def nakedtrader(request):

    context = [{
        "symbol": nt.stock.Symbol,
        "qty": nt.qty,
        "price": nt.price,
        "target": nt.target,
        "stop": nt.stop,
        "buy_date": nt.buy_date.strftime("%d-%b-%Y"),
        "sell": nt.sell,
        "sell_date": nt.sell_date.strftime("%d-%b-%Y"),
        "pl": nt.pl,
    } for nt in StockNT.objects.all().order_by('-buy_date')[:100]]

    return addCORSHeaders(
        HttpResponse(json.dumps(context))
    )


def loginRequest(request, username, password):
    user = authenticate(username=username, password=password)
    response = {'success':False}
    if user:
        # the password verified for the user
        if user.is_active:
            response['success'] = True
        else:
            response['message'] = "The password is valid, but the account has been disabled!"
    else:
        # the authentication system was unable to verify the username and password
        response['message'] = "The username and password were incorrect."

    return addCORSHeaders(
        HttpResponse(json.dumps(response))
    )

# client views
class PostHandlerView(generic.TemplateView):
    def post(self, request, *args, **kwargs):
        kwargs['post'] = self.request.POST
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class AccountView(PostHandlerView):
    template_name = 'market/account.html'

    def get_context_data(self, **kwargs):
        context = {'navRoutes':navRoutes()}

        return context

class SelectionView(PostHandlerView):
    template_name = 'market/selection.html'

    def get_context_data(self, **kwargs):
        context = {'navRoutes':navRoutes()}
        context['StockFav'] =  [sel.stock for sel in StockSelection.objects.filter(user=self.request.user)]
        return context


class NewsView(PostHandlerView):
    template_name = 'market/news.html'

    def get_context_data(self, **kwargs):
        dt = timezone.now()
        past = dt + datetime.timedelta(days=-1)
        context = {'navRoutes':navRoutes()}
        context['AllNews'] = StockNews.objects.filter(pub_date__gte=past).order_by('-pub_date')
        return context


class SectorView(PostHandlerView):
    template_name = 'market/sector.html'

    def get_context_data(self, **kwargs):
        context = {'navRoutes':navRoutes()}
        context['sectors'] = [{'name':sn, 'id':'Sect{:02d}'.format(id)} for (sn, id) in zip(sector_names, range(len(sector_names)))]
        return context


class IndexView(PostHandlerView):
    template_name = 'market/index.html'

    def get_context_data(self, **kwargs):
        context = {'navRoutes':navRoutes()}

        context['Stocks'] = common_filter(Stock.objects, trend=False, mch=9999999)

        favstocks = [
            sel.stock for sel in StockSelection.objects.filter(
                user=self.request.user
            )
        ]

        favnews = []
        dt = timezone.now()
        past = dt + datetime.timedelta(days=-2)
        for stock in favstocks:
            favnews += [
                news for news in StockNews.objects.filter(stock=stock, pub_date__gte=past).order_by('-pub_date')
            ]

        context['favNews'] = favnews
        context['NTStocks'] = StockNT.objects.all().order_by('-buy_date')[:100]

        return context


class DetailView(PostHandlerView):
    template_name = 'market/details.html'

    def get_context_data(self, **kwargs):
        context = {'navRoutes':navRoutes()}

        if kwargs and kwargs.get('post'):
            username = kwargs.get('post').get('username')
            symbol = kwargs['symbol']
            track_stats = kwargs.get('post').get('track')

            if track_stats == 'false':
                user = User.objects.get(username=username)
                stock = Stock.objects.get(Symbol=symbol)
                selection = StockSelection(user=user, stock=stock)
                selection.save()
            else:
                StockSelection.objects.filter(user__username=username, stock__Symbol=symbol).delete()


        if kwargs and kwargs['symbol']:
            detail = get_object_or_404(Stock, Symbol=kwargs['symbol'].upper())
            context['stockdetail'] = detail
            context['stocknews'] = StockNews.objects.filter(stock=detail).order_by('-pub_date')[:10]

        return context


class ListView(PostHandlerView):
    template_name = 'market/list.html'

    dt = timezone.now()
    past = dt + datetime.timedelta(days=-2)

    def get_context_data(self, **kwargs):

        if self.request.session.get('filtered') is None:
            self.request.session['filtered'] = True

        if kwargs and kwargs.get('post'):
            self.request.session['filtered'] = (kwargs.get('post').get('stockFilter')=='on')

        isFiltered = self.request.session.get('filtered')

        context = {
            'navRoutes':navRoutes(),
            'isFiltered':'checked' if isFiltered else '',
            'StockFTSEALL':[],
            'StockFTSEAIMALL':[],
        }

        if kwargs and kwargs.get('catagory'):
            if kwargs['catagory'] == 'ftse':
                context['StockFTSEALL'] = Stock.objects.filter(Catagory__contains='FTSE All-Share')
            elif kwargs['catagory'] == 'ftseaim':
                context['StockFTSEAIMALL'] = Stock.objects.filter(Catagory__contains='FTSE AIM All-Share')
        else:
            context['StockFTSEALL'] = Stock.objects.filter(Catagory__contains='FTSE All-Share')
            context['StockFTSEAIMALL'] = Stock.objects.filter(Catagory__contains='FTSE AIM All-Share')

        if context['StockFTSEALL'] and isFiltered:
            context['StockFTSEALL'] = common_filter(context['StockFTSEALL'], update_date=self.past)

        if context['StockFTSEAIMALL'] and isFiltered:
            context['StockFTSEAIMALL'] = common_filter(context['StockFTSEAIMALL'], update_date=self.past)

        return context
