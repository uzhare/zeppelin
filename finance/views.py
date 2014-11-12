from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Ticker
import requests
from lxml import etree
import json

class TickerListView(ListView):
    queryset = Ticker.objects.all()[:50]
    context_object_name = "ticker_list"
    template_name = "finance/ticker_list.html"

    def __init__(self, *args, **kwargs):
        return super(TickerListView,
            self).__init__(*args, **kwargs)

    def get_queryset(self):
        return super(TickerListView, 
            self).get_queryset()


class DisplayView(TemplateView):
    template_name = 'finance/display.html'
    success_url = ''

    def get(self, request, *args, **kwargs):
        ticker = kwargs['ticker']
        ticker_object = Ticker.objects.get(id=ticker)
        url = "http://download.finance.yahoo.com/d/quotes.csv?s=%40%5EDJI,%s&f=nsl1op&e=.csv" % ticker_object.ticker
        data = requests.get(url, stream=True)
        
        with open('help.csv', 'wb') as f:
            for chunk in data.iter_content(1024):
                f.write(chunk)
        import csv
        with open('help.csv', 'rb') as f:
            read = csv.reader(f, delimiter=',', quotechar='"')
            for row in read:
                result = row
        print result
        kwargs.update({'result': result,})
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)