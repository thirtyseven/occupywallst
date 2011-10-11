import urllib2, urllib
import csv

from django.db import IntegrityError
from django.core.management.base import BaseCommand, CommandError

from occupywallst.models import StockData

SYMBOLS=['^DJI', '^GSPC', "^IXIC"]
API_URL="http://ichart.finance.yahoo.com/table.csv?"

def get_stock_data(symbols):
    params = { "g":'d', "a":8, "b":13, "c":2011 }
    for symb in symbols:
        params['s']=symb
        try:
            data = urllib2.urlopen(API_URL+ urllib.urlencode(params))
        except urllib2.HTTPError as e:
            print e.geturl()
            print dir(e)
            raise e
        reader = csv.DictReader(data)
        for row in reader:
            try:
                if StockData.objects.filter(symb=symb, date=row['Date']):
                    continue
                sd = StockData()
                sd.symb = symb
                sd.date = row['Date']
                sd.open = row['Open'].replace('.','')
                sd.close = row['Close'].replace('.','')
                sd.high = row['High'].replace('.','')
                sd.low = row['Low'].replace('.','')
                sd.volume = row['Volume']
                sd.save()
            except IntegrityError:
                pass

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        get_stock_data(SYMBOLS)
