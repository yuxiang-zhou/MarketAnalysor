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
    if theHttpResponse and isinstance(theHttpResponse, HttpResponse):
        theHttpResponse['Access-Control-Allow-Origin'] = '*'
        theHttpResponse['Access-Control-Max-Age'] = '120'
        theHttpResponse['Access-Control-Allow-Credentials'] = 'true'
        theHttpResponse['Access-Control-Allow-Methods'] = 'HEAD, GET, OPTIONS, POST, DELETE'
        theHttpResponse['Access-Control-Allow-Headers'] = 'origin, content-type, accept, x-requested-with'
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
