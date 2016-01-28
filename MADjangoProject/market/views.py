from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.core import serializers

from .models import Stock, StockHistory

navRoutes = [{
    'path':'/market',
    'isActive':False,
    'icon':'fa-home',
    'label':'Summary',
    'children': []
},{
    'path':'/market/list',
    'isActive':False,
    'icon':'fa-table',
    'label':'Stock Table',
    'children': [{
        'path':'/market/list/ftse',
        'isActive':False,
        'icon':'fa-table',
        'label':'FTSE ALL',
        'children': []
    },{
        'path':'/market/list/ftseaim',
        'isActive':False,
        'icon':'fa-table',
        'label':'FTSE AIM ALL',
        'children': []
    }]
}]

def history(request, symbol):
    return HttpResponse(serializers.serialize('json', Stock.objects.get(Symbol=symbol).stockhistory_set.all()))

class IndexView(generic.TemplateView):
    template_name = 'market/index.html'

    def get_context_data(self, **kwargs):
        return {'navRoutes':navRoutes}

class DetailView(generic.TemplateView):
    template_name = 'market/details.html'

    def get_context_data(self, **kwargs):
        context = {'navRoutes':navRoutes}

        if kwargs and kwargs['symbol']:
            context['stockdetail'] = Stock.objects.get(Symbol=kwargs['symbol'])

        return context

class ListView(generic.TemplateView):
    template_name = 'market/list.html'

    def get_context_data(self, **kwargs):
        context = {'navRoutes':navRoutes, 'StockFTSEALL':[], 'StockFTSEAIMALL':[]}

        if kwargs and kwargs['catagory']:
            if kwargs['catagory'] == 'ftse':
                context['StockFTSEALL'] = Stock.objects.filter(Catagory__contains='FTSE All-Share')
            elif kwargs['catagory'] == 'ftseaim':
                context['StockFTSEAIMALL'] = Stock.objects.filter(Catagory__contains='FTSE AIM All-Share')
        else:
            context['StockFTSEALL'] = Stock.objects.filter(Catagory__contains='FTSE All-Share')
            context['StockFTSEAIMALL'] = Stock.objects.filter(Catagory__contains='FTSE AIM All-Share')

        if context['StockFTSEALL']:
            context['StockFTSEALL'] = context['StockFTSEALL'].filter(MarketCap__gte=49).filter(MarketCap__lte=1000).filter(MPRatio__lte=20).filter(Spread__lte=3).filter(Liquidity__gte=2000).filter(ProfitTrend__gte=0).filter(DividendTrend__gte=0).filter(DebtTrend__gte=0).filter(DPRatio__lte=3)

        if context['StockFTSEAIMALL']:
            context['StockFTSEAIMALL'] = context['StockFTSEAIMALL'].filter(MarketCap__gte=49).filter(MarketCap__lte=1000).filter(MPRatio__lte=20).filter(Spread__lte=3).filter(Liquidity__gte=2000).filter(ProfitTrend__gte=0).filter(DividendTrend__gte=0).filter(DebtTrend__gte=0).filter(DPRatio__lte=3)

        return context
