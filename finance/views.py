from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Ticker
import requests
from lxml import etree
import json

class TickerListView(ListView):
    queryset = Ticker.objects.all()
    context_object_name = "ticker_list"
    template_name = "finance/ticker_list.html"

    def __init__(self, *args, **kwargs):
        # This is a temporary work around. Extracting ticker list 
        # and saving the objects must be a background task.

        TICKER_LIST_URL = "http://query.yahooapis.com/v1/public/yql?q=" + \
                          "select * from yahoo.finance.industry where id in" + \
                          "(select industry.id from yahoo.finance.sectors)" + \
                          "&env=store://datatables.org/alltableswithkeys"
        ticker_page = requests.get(TICKER_LIST_URL)
        ticker_text = ticker_page.text.encode('utf-8')
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        tree = etree.fromstring(ticker_text, parser=parser)
        industries =  tree.xpath('results/industry')
        ticker_list = []
        symbol_list = []
        
        for industry in industries:
            symbol = industry.xpath('company/@symbol')
            name = industry.xpath('company/@name')
            result = zip(symbol, name)
            symbol_list.append(result)
        # Limiting the list for testing/and for dummy app.
        for ticker in symbol_list[1][:10]:
            ticker_object = Ticker()
            
            try:
                obj = Ticker.objects.get(ticker=ticker)
            except Ticker.DoesNotExist:
                    ticker_object.ticker = ticker[0] or ''
                    ticker_object.company_name = ticker[1] or ''
                    ticker_object.save()
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