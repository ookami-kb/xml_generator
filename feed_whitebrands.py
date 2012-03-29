# -*- coding: utf-8 -*-
from xml_generator.models import *
#goods = { 1: u'Говядина', 2 : u'Масло подсолнечное', 6 : u'Пшено', 7 : u'Морковь', 8 : u'Баранина',  9 : u'Яблоки', 10 : u'Картофель', 11: u'Рыба', 12 : u'Соль поваренная пищевая', 13 : u'Чай чёрный байховый', 14 : u'Мука пшеничная', 15 : u'Лук репчатый', 16 : u'Капуста белокочанная', 17 : u'Куры', 18 : u'Хлеб ржаной', 19 : u'Молоко', 21 :u'Рис', 22 : u'Крупа гречневая', 23 : u'Вермишель', 24 : u'Сахар-песок', 25 : u'Масло сливочное',  26 : u'Яйца куриные', 27 : u'Свинина',  28 : u'Хлеб пшеничный'}

goods = { 1: 'Говядина', 2 : 'Масло подсолнечное', 6 : 'Пшено', 7 : 'Морковь',
          8 : 'Баранина',  9 : 'Яблоки', 10 : 'Картофель', 11: 'Рыба',
          12 : 'Соль поваренная пищевая', 13 : 'Чай чёрный байховый', 14 : 'Мука пшеничная',
          15 : 'Лук репчатый', 16 : 'Капуста белокочанная', 17 : 'Куры', 18 : 'Хлеб ржаной',
          19 : 'Молоко', 21 :'Рис', 22 : 'Крупа гречневая', 23 : 'Вермишель', 24 : 'Сахар-песок',
          25 : 'Масло сливочное',  26 : 'Яйца куриные', 27 : 'Свинина',  28 : 'Хлеб пшеничный'}

for key in goods.iterkeys():
    wb = WhiteBrand(ext_id = key, name = goods[key])
    wb.save()


#--------------------Organizations
from xml_generator.models import *
import urllib2
import simplejson
#req = urllib2.Request("http://192.168.139.121:8001/api/v1/organization/?format=json&limit=0", None, {'user-agent':'syncstream/vimeo'})
req = urllib2.Request("http://127.0.0.1:8800/api/v1/organization/?format=json&limit=0", None, {'user-agent':'syncstream/vimeo'})

opener = urllib2.build_opener()
f = opener.open(req)

s = simplejson.load(f)

for obj in s['objects']:
    sp = Organization(name=  obj['name'], pk = obj['id'])
    sp.save()


#-----------------------Salepoints

#8800 port!!

from xml_generator.models import *
import urllib2
import simplejson
#req = urllib2.Request("http://192.168.139.121:8001/api/v1/station/?format=json&limit=0", None, {'user-agent':'syncstream/vimeo'})
req = urllib2.Request("http://127.0.0.1:8800/api/v1/station/?format=json&limit=0", None, {'user-agent':'syncstream/vimeo'})

opener = urllib2.build_opener()
f = opener.open(req)

s = simplejson.load(f)

for obj in s['objects']:
    org = Organization.objects.get(pk=obj['organization_id'])
    sp = Salepoint(pk=int(obj['id']), name=obj['name'], address=obj['address'], city=obj['city'],
                   latitude=obj['lat'], longitude=obj['lon'], status = obj['status'], is_new = False,
                   organ=org, pricelist_name=obj['pricelist_name'], pricelist_url=obj['pricelist_url'], point_type=obj['point_type'])
    sp.save()





#------------------------------------Products

from xml_generator.models import *
import urllib2
import simplejson
#req = urllib2.Request("http://192.168.139.121:8001/api/v1/products/?format=json&limit=0", None, {'user-agent':'syncstream/vimeo'})
req = urllib2.Request("http://127.0.0.1:8800/api/v1/products/?format=json&limit=0", None, {'user-agent':'syncstream/vimeo'})

opener = urllib2.build_opener()
f = opener.open(req)

s = simplejson.load(f)
for obj in s['objects']:
    try:
        try:
            wb = WhiteBrand.objects.get(pk=obj['whitebrand_id'])
            #print wb.pk
        except:
            wb = None


        pr = Product(title = obj['title'], title_extra = obj['title_extra'], source_code = obj['source_code'], source_type = obj['source_type'],
            manufacturer = obj['manufacturer'], white_brand = wb, is_new = False)
        pr.save()
        #print pr.pk
    except Exception as e:
        print str(e)






