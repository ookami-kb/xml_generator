__author__ = 'eugene'
from xml_generator.models import *
import urllib2
import simplejson
from django.utils.timezone import utc
from datetime import datetime

i = 0
j = 150
while i < 1800:
    _url = "http://127.0.0.1:8800/api/v1/products_offers/?format=json&limit=" + str(j) +"&offset=" + str(i)
    req = urllib2.Request(_url, None, {'user-agent':'syncstream/vimeo'})
    opener = urllib2.build_opener()
    f = opener.open(req)
    s = simplejson.load(f)
    for obj in s['objects']:
        try:
            for _sp in obj['salepoints']:
                sp = Salepoint.objects.get(pk=_sp)
                pr = Product.objects.get(source_code=int(obj['source_code']), source_type=obj['source_type'])
                off = Offer(product=pr, salepoint=sp, price=obj['price'], created=datetime.utcnow().replace(tzinfo=utc))
                off.save()
        except Exception as e:
            print str(e)
    print str(i)
    print str(j)
    i += 150


