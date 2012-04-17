__author__ = 'eugene'
# -*- coding: utf-8 -*-
from xml_generator.models import *
from django.core.management.base import BaseCommand, CommandError
import urllib2
import simplejson
from django.utils.timezone import utc
from datetime import datetime
from optparse import make_option


class Command(BaseCommand):
    args = ''
    help = 'get all offers'


    def handle(self, *args, **options):
        try:
            goods = { 1: ['Говядина', 'weight', 'кг', 1],
                      2 : ['Масло подсолнечное', 'volume', 'л', 1],
                      6 : ['Пшено', 'weight', 'кг', 1],
                      7 : ['Морковь', 'weight', 'кг', 1],
                      8 : ['Баранина', 'weight', 'кг', 1],
                      9 : ['Яблоки', 'weight', 'кг', 1],
                      10 : ['Картофель', 'weight', 'кг', 1],
                      11: ['Рыба', 'weight', 'кг', 1],
                      12 : ['Соль поваренная пищевая', 'weight', 'кг', 1],
                      13 : ['Чай чёрный байховый', 'weight', 'кг', 1],
                      14 : ['Мука пшеничная', 'weight', 'кг', 1],
                      15 : ['Лук репчатый', 'weight', 'кг', 1],
                      16 : ['Капуста белокочанная', 'weight', 'кг', 1],
                      17 : ['Куры', 'weight', 'кг', 1],
                      18 : ['Хлеб ржаной', 'weight', 'кг', 1],
                      19 : ['Молоко', 'volume', 'л', 1],
                      21 :['Рис','weight', 'кг', 1],
                      22 : ['Крупа гречневая','weight', 'кг', 1],
                      23 : ['Вермишель','weight', 'кг', 1],
                      24 : ['Сахар-песок','weight', 'кг', 1],
                      25 : ['Масло сливочное','weight', 'кг', 1],
                      26 : ['Яйца куриные','amount', 'шт', 10],
                      27 : ['Свинина','weight', 'кг', 1],
                      28 : ['Хлеб пшеничный','weight', 'кг', 1]}

            for key in goods.iterkeys():
                wb = WhiteBrand(ext_id = key, name = goods[key][0], factor_specific_key = goods[key][1], factor_specific_unit = goods[key][2], factor_specific_value=goods[key][3])
                wb.save()



            #req = urllib2.Request("http://192.168.139.121:8001/api/v1/organization/?format=json&limit=0", None, {'user-agent':'syncstream/vimeo'})
            req = urllib2.Request("http://v-zabote.ru/api/v1/organization/?format=json&limit=0", None, {'user-agent':'syncstream/vimeo'})

            opener = urllib2.build_opener()
            f = opener.open(req)

            s = simplejson.load(f)

            for obj in s['objects']:
                sp = Organization(name=  obj['name'], pk = obj['id'])
                sp.save()


            req = urllib2.Request("http://v-zabote.ru/api/v1/station/?format=json&limit=0", None, {'user-agent':'syncstream/vimeo'})

            opener = urllib2.build_opener()
            f = opener.open(req)

            s = simplejson.load(f)

            for obj in s['objects']:
                org = Organization.objects.get(pk=obj['organization_id'])
                sp = Salepoint(pk=int(obj['id']), name=obj['name'], address=obj['address'], city=obj['city'],
                    latitude=obj['lat'], longitude=obj['lon'], status = obj['status'], is_new = False,  is_redundant=False,
                    organ=org,  point_type=obj['point_type'])
                #pricelist_name=obj['pricelist_name'], pricelist_url=obj['pricelist_url'],
                sp.save()


            req = urllib2.Request("http://v-zabote.ru/api/v1/products/?format=json&limit=0", None, {'user-agent':'syncstream/vimeo'})

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

                    manuf = Manufacturer(name=obj['manufacturer'])
                    manuf.save()
                    _count = Country(name=obj['country'])
                    _count.save()
                    pr = Product(title = obj['title'], title_extra = obj['title_extra'], source_code = obj['source_code'], source_type = obj['source_type'],
                        manufacturer = manuf, country = _count, type=obj['type'], white_brand = wb, is_new = False, is_redundant=False)
                    pr.save()
                    #print pr.pk
                except Exception as e:
                    print str(e)


            i = 0
            j = 400
            while i < 10000:
                _url = "http://v-zabote.ru/api/v1/products_offers/?format=json&limit=" + str(j) +"&offset=" + str(i)
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
                #print str(j)
                i += 400
        except Exception as e:
            raise CommandError('Some error detected: "%s" ' % str(e))