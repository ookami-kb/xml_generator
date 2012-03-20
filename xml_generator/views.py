__author__ = 'eugene'
# -*- coding: utf-8 -*-

from django.utils import simplejson
from django.http import HttpResponse
import os, shutil
from lxml import etree
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
global_path = settings.GLOBAL_PATH
from xml_generator.models import *

@csrf_exempt
def generate_xml(request):

    if not os.path.exists(global_path):
        os.makedirs(global_path)

    organs = Organization.objects.all()

    user_name = 'eugene'
    user_path = global_path + '/' + user_name + '/pricelists/'
    if os.path.exists(user_path):
        shutil.rmtree(user_path)
    os.makedirs(user_path)


    for org in organs:

        outDir = user_path + 'org-%s/' % (org.pk)
        if os.path.exists(outDir):
            shutil.rmtree(outDir)
        os.makedirs(outDir)


        NOL = etree.Element('pricelists')

        for sp in org.salepoint_set.all():
            pricelist = etree.SubElement(NOL, 'pricelist')


            pr_name = etree.SubElement(pricelist, 'name')
            pr_name.text = sp.pricelist_name



            pr_url = etree.SubElement(pricelist, 'url')
            pr_url.text = sp.pricelist_url

            pr_ishop = etree.SubElement(pricelist, 'ishop')
            pr_ishop.text = u"http://seller.ru/"

            pr_shops = etree.SubElement(pricelist, 'shops')

            shop = etree.SubElement(pr_shops, 'shop')

            sh_city = etree.SubElement(shop, 'city')
            sh_city.text = u'Челябинск'

            sh_name = etree.SubElement(shop, 'name')
            sh_name.text = sp.name

            sh_address = etree.SubElement(shop, 'address')
            sh_address.text = sp.address

            sh_coord = etree.SubElement(shop, 'coord')
            sh_lat = etree.SubElement(sh_coord, 'latitude')
            sh_lat.text = unicode(sp.latitude)
            sh_lon = etree.SubElement(sh_coord, 'longitude')
            sh_lon.text = unicode(sp.longitude)


            NPL = etree.Element('offers')
            _offers = Offer.objects.filter(salepoint=sp)
            for _offer in _offers:
                offer = etree.SubElement(NPL, 'offer')
                price = etree.SubElement(offer, 'price')
                price.text = unicode(_offer.price)

                code = etree.SubElement(offer, 'code')
                code.set('source', _offer.product.source_type)
                code.text = unicode(_offer.product.source_code)

            structureXml = open(outDir +pr_name.text +'.xml', "w")
            structureXml.write(etree.tostring(NPL, pretty_print=True, encoding="utf8"))
            structureXml.close()


        structureXml = open(outDir + 'index.xml', "w")
        structureXml.write(etree.tostring(NOL, pretty_print=True, encoding="utf8"))
        structureXml.close()

        content = simplejson.dumps({'status' : 'OK,'})
    return HttpResponse(content, mimetype='application/javascript')



