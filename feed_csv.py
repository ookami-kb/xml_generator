# -*- coding: utf-8 -*-
__author__ = 'eugene'

import csv
from xml_generator.models import *


from datetime import datetime
from django.utils.timezone import utc

sr = csv.reader(open('/home/eugene/Documents/xml_generator/xml_generator/offers.csv', 'rb'),delimiter=',')
headers = sr.next()
i = 100000
for row in sr:

    try:
        sp = Salepoint.objects.get(address=unicode(row[2], 'utf-8'))
        print 'y'
    except:
        try:
            org =  Organization.objects.filter(name=unicode(row[6], 'utf-8'))[0]
        except:
            org = Organization(pk = int(unicode(row[5], 'utf-8')),name=unicode(row[6], 'utf-8') )
            org.save()
        print 'b'
        try:
            latitude=float(unicode(row[4], 'utf-8'))
            longitude=float(unicode(row[3], 'utf-8'))
        except:
            latitude = 0
            longitude = 0

        sp = Salepoint(name=unicode(row[1], 'utf-8'), is_new=False, address=unicode(row[2], 'utf-8'), latitude=latitude, longitude=longitude, organ=org)
        #i+=1
        print sp
        sp.save()
    try:
        pr = Product.objects.filter(source_code=unicode(row[7], 'utf-8'), white_brand__ext_id=int(unicode(row[8], 'utf-8')))[0]
    except:
        pr = Product.objects.filter(source_code=unicode(row[7], 'utf-8'))[0]

    of = Offer(salepoint=sp, product=pr, price=float(unicode(row[0], 'utf-8')), is_redundant=False, created=datetime.utcnow().replace(tzinfo=utc))
    of.save()
    #print of

print 'ok'
'''
In [18]: headers
Out[18]: 
['price',0
 'salepoint_name',1
 'salepoint_address',2
 'lon',3
 'lat',4
 'id',5
 'name_org',6
 'source_code',7
 'white_brand_id']8

'''
