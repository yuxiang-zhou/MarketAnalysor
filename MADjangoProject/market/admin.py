from django.contrib import admin

from django.contrib.auth.models import User
from .models import Stock, StockHistory, StockSelection, SectorHistory, StockNews

class CommonAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'

class SectorAdmin(CommonAdmin):
    list_display = ('Symbol', 'Sector', 'pub_date')
    search_fields = ['Symbol', 'Sector']

class StockAdmin(CommonAdmin):
    list_display = ('Symbol', 'Name','MarketCap', 'Catagory', 'pub_date')
    search_fields = ['Symbol']

class StockRelativeAdmin(CommonAdmin):
    def stock_info(obj):
        return '{}, {}, {}, {}'.format(
            obj.stock.Symbol,
            obj.stock.Name,
            obj.stock.MarketCap,
            obj.stock.pub_date,
        )

    list_display = (stock_info, 'pub_date')
    search_fields = ['stock__Symbol']



admin.site.register(Stock, StockAdmin)
admin.site.register(SectorHistory, SectorAdmin)
admin.site.register(StockHistory, StockRelativeAdmin)
admin.site.register(StockSelection, StockRelativeAdmin)
admin.site.register(StockNews, StockRelativeAdmin)
