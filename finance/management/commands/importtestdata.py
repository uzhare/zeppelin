
from django.core.management.base import BaseCommand, CommandError

from finance.models import Ticker
import requests
from lxml import etree

class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **kwargs):
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
