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
    help = 'specific import of offers'

    def handle(self, *args, **options):
        try:
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





            i = 0
            j = 400
            while i < 12000:
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
                            off = Offer(product=pr, salepoint=sp, price=obj['price'], created=datetime.fromtimestamp(obj['timestamp']))
                            off.save()
                    except Exception as e:
                        print str(e)
                print str(i)
                #print str(j)
                i += 400

        except Exception as e:
            raise CommandError('Blaaa: "%s" ' % str(e))