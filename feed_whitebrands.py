# -*- coding: utf-8 -*-
from xml_generator.models import *
goods = { 1: u'Говядина', 2 : u'Масло подсолнечное', 6 : u'Пшено', 7 : u'Морковь', 8 : u'Баранина',  9 : u'Яблоки', 10 : u'Картофель', 11: u'Рыба', 12 : u'Соль поваренная пищевая', 13 : u'Чай чёрный байховый', 14 : u'Мука пшеничная', 15 : u'Лук репчатый', 16 : u'Капуста белокочанная', 17 : u'Куры', 18 : u'Хлеб ржаной', 19 : u'Молоко', 21 :u'Рис', 22 : u'Крупа гречневая', 23 : u'Вермишель', 24 : u'Сахар-песок', 25 : u'Масло сливочное',  26 : u'Яйца куриные', 27 : u'Свинина',  28 : u'Хлеб пшеничный'}


for key in goods.iterkeys():
    wb = WhiteBrand(ext_id = key, name = goods[key])
    wb.save()

#-----------------------Salepoints

#8800 port!!

from xml_generator.models import *
import urllib2
import simplejson
req = urllib2.Request("http://127.0.0.1:8800/api/v1/station/?format=json&limit=0", None, {'user-agent':'syncstream/vimeo'})

opener = urllib2.build_opener()
f = opener.open(req)

s = simplejson.load(f)

for obj in s['objects']:
    org = Organization.objects.get(pk=obj['organization_id'])
    sp = Salepoint(name=obj['name'], address=obj['address'], 
                   latitude=obj['lat'], longitude=obj['lon'], 
                   organ=org)
    sp.save()



#--------------------Organizations
from xml_generator.models import *
import urllib2
import simplejson
req = urllib2.Request("http://127.0.0.1:8800/api/v1/organization/?format=json&limit=0", None, {'user-agent':'syncstream/vimeo'})

opener = urllib2.build_opener()
f = opener.open(req)

s = simplejson.load(f)

for obj in s['objects']:
    sp = Organization(name=  obj['name'], pk = obj['id'])
    sp.save()



#-----------------------Offers
from xml_generator.models import *
import urllib2
import simplejson
req = urllib2.Request("http://127.0.0.1:8800/api/v1/products_offers/?format=json&limit=15", None, {'user-agent':'syncstream/vimeo'})

opener = urllib2.build_opener()
f = opener.open(req)

s = simplejson.load(f)

for obj in s['objects']:
    sp = Salepoint(name=  obj['name'], address = obj['address'] , latitude = obj['lat'], longitude = obj['lon'], organ = obj['organization_id'])
    sp.save()
