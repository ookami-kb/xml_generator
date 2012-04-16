
import csv
from xml_generator.models import *


from datetime import datetime
from django.utils.timezone import utc

sr = csv.reader(open('/home/eugene/Documents/xml_generator/xml_generator/offers.csv', 'rb'),delimiter=',')
headers = sr.next()


for row in sr:
    try:
      try:
	  sp = Salepoint.objects.get(address=unicode(row[2], 'utf-8'))
      except:
	  org, created = Organization.objects.get_or_create(name=unicode(row[6], 'utf-8')) 
	  sp = Salepoint(name=unicode(row[1]).encode('utf-8'), is_new=False, address=unicode(row[2]).encode('utf-8'), latitude=float(unicode(row[4]).encode('utf-8')), longitude=float(unicode(row[3], 'utf-8')), organ=org)
	  print sp
	  sp.save()
      try:
	  pr = Product.objects.filter(source_code=unicode(row[7], 'utf-8'), white_brand__ext_id=int(unicode(row[8], 'utf-8')))[0]
      except:
	  pr = Product.objects.filter(source_code=unicode(row[7], 'utf-8'))[0]
      of = Offer(salepoint=sp, product=pr, price=float(unicode(row[0], 'utf-8')), is_redundant=False, created=datetime.utcnow().replace(tzinfo=utc))
      of.save()
      print 'a'
    except:
      print 'call'