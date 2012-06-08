__author__ = 'eugene'
# -*- coding: utf-8 -*-

from django.utils import simplejson
from django.http import HttpResponse
import os, shutil
from lxml import etree
import csv

from django.conf import settings
global_path = settings.GLOBAL_PATH
from xml_generator.models import *
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    args = ''
    help = 'generatexml'

    def handle(self, *args, **options):


        try:
            if not os.path.exists(global_path):
                os.makedirs(global_path)
            else:
                shutil.rmtree(global_path)

            organs = Organization.objects.all()
            user_path = global_path + '/pricelists/'
            if os.path.exists(user_path):
                shutil.rmtree(user_path)
            os.makedirs(user_path)

            AU = etree.Element('au')
            OU = etree.Element('ou')
            ofile = open(user_path +'ocsv.csv', 'wb')
            ocsv = csv.writer(ofile, delimiter=',')
            afile = open(user_path +'acsv.csv', 'wb')
            acsv = csv.writer(afile, delimiter=',')

            k = 0
            of_count = 0
            for org in organs:
                if org.pk == 1:
                    continue
                outDir = user_path + 'org-%s/' %  org.pk
                if os.path.exists(outDir):
                    shutil.rmtree(outDir)
                os.makedirs(outDir)

                part2 = etree.SubElement(OU, 'part')
                part_a2 = etree.SubElement(part2, 'name')
                part_a2.text = org.name
                part_u2 = etree.SubElement(part2, 'url')
                part_u2.text = 'ftp://upload.v-zabote.ru/data/pricelists/'+ ('org-%s/' %  org.pk) + 'index.xml'
                ocsv.writerow([unicode(org.name).encode('utf-8'),unicode(org.pk).encode('utf-8'), 'ftp://upload.v-zabote.ru/data/pricelists/'+ ('org-%s/' %  org.pk) + 'index.xml'])




                NOL = etree.Element('pricelists')
                orgs = org.salepoint_set.filter(is_redundant=False, is_new=False)
                k+= orgs.count()

                for sp in orgs:
                    pricelist = etree.SubElement(NOL, 'pricelist')
                    pr_name = etree.SubElement(pricelist, 'name')
                    pr_name.text = sp.name
                    pr_url = etree.SubElement(pricelist, 'url')
                    #pr_url.text = sp.pricelist_url
                    #pr_url.text = (sp.pricelist_url.split('/')[-1].split('.')[0] + '.xml') if sp.pricelist_url else 'price-' + str(sp.pk) + '.xml'
                    pr_url.text = 'price-' + str(sp.pk) + '.xml'
                    #pr_ishop = etree.SubElement(pricelist, 'ishop')
                    #pr_ishop.text = u"http://seller.ru/"
                    pr_shops = etree.SubElement(pricelist, 'shops')

                    shop = etree.SubElement(pr_shops, 'shop')
                    shop.set('type', sp.point_type)
                    sh_name = etree.SubElement(shop, 'name')
                    sh_name.text = sp.name
                    sh_city = etree.SubElement(shop, 'city')
                    #sh_city.text = u'Челябинск'
                    sh_city.text  = sp.city
                    sh_address = etree.SubElement(shop, 'address')
                    sh_address.text = sp.address

                    sh_coord = etree.SubElement(shop, 'coord')
                    sh_lat = etree.SubElement(sh_coord, 'latitude')
                    sh_lat.text = unicode(sp.latitude)
                    sh_lon = etree.SubElement(sh_coord, 'longitude')
                    sh_lon.text = unicode(sp.longitude)

                    part = etree.SubElement(AU, 'part')
                    part_a = etree.SubElement(part, 'address')
                    part_a.text = sp.address
                    part_n = etree.SubElement(part, 'name')
                    part_n.text = sp.name
                    part_pk = etree.SubElement(part, 'id')
                    part_pk.text = unicode(sp.pk)
                    part_u = etree.SubElement(part, 'url')
                    part_u.text = 'ftp://upload.v-zabote.ru/data/pricelists/'+ ('org-%s/' %  org.pk) + 'price-' + str(sp.pk) + '.xml'
                    acsv.writerow([unicode(sp.address).encode('utf-8'),unicode(sp.name).encode('utf-8'),unicode(sp.pk).encode('utf-8'), 'ftp://upload.v-zabote.ru/data/pricelists/'+ ('org-%s/' %  org.pk) + 'price-' + str(sp.pk) + '.xml'])




                    NPL = etree.Element('offers')
                    _offers = Offer.objects.filter(salepoint=sp, product__is_new=False, price__gt=0, product__is_redundant=False, is_redundant=False)
                    #print _offers.query
                    of_count += _offers.count()
                    for _offer in _offers:
                        offer = etree.SubElement(NPL, 'offer')
                        price = etree.SubElement(offer, 'price')
                        price.text = unicode(_offer.price)
                        _date = etree.SubElement(offer, 'date')
                        _date.text = datetime.strftime(_offer.created, "%d.%m.%Y %H:%M:%S")
                        code = etree.SubElement(offer, 'code')
                        code.set('source', _offer.product.source_type)
                        code.text = unicode(_offer.product.source_code)

                    structureXml2 = open(outDir + 'price-' + str(sp.pk) + '.xml', 'w')#pr_name.text +'.xml', "w")
                    #print NPL
                    structureXml2.write(etree.tostring(NPL, pretty_print=True, encoding="cp1251", xml_declaration=True))
                    structureXml2.close()



                #if len(org.salepoint_set.all()) > 0:
                structureXml = open(outDir + 'index.xml', "w")
                structureXml.write(etree.tostring(NOL, pretty_print=True, encoding="cp1251", xml_declaration=True))
                structureXml.close()

            structureXml = open(user_path + 'au.xml', 'w')#pr_name.text +'.xml', "w")
            structureXml.write(etree.tostring(AU, pretty_print=True, encoding="cp1251", xml_declaration=True))
            structureXml.close()


            structureXml = open(user_path + 'ou.xml', 'w')#pr_name.text +'.xml', "w")
            structureXml.write(etree.tostring(OU, pretty_print=True, encoding="cp1251", xml_declaration=True))
            structureXml.close()

            #NNPL: notation new product language
            NNPL =  etree.Element('source')
            NNPL.set('data_source_name', 'neiron')
            prs = Product.objects.filter(is_new=False, is_redundant=False)
            for product in prs:
                _pr = etree.SubElement(NNPL, 'product')
                _pr.set('name', product.title)
                _pr.set('id', str(product.source_code))


            for country in Country.objects.all().distinct():
                _cunt = etree.SubElement(NNPL, 'country')
                _cunt.set('name', country.name)
                _cunt.set('id', str(country.pk))

            for _mf in Manufacturer.objects.all().exclude(name=None).distinct():
                _mfuck  = etree.SubElement(NNPL, 'manufacturer')
                _mfuck.set('name', _mf.name)
                _mfuck.set('id', str(_mf.pk))

            prs = Product.objects.filter(is_new=False, is_redundant=False).exclude(manufacturer=None)
            for product in prs:
                _modif = etree.SubElement(NNPL, 'modification')
                _modif.set('id', str(product.source_code))
                _modif.set('title', product.title)
                if product.title_extra:
                    _modif.set('title_extra', product.title_extra)
                else: _modif.set('title_extra', '')
                _modif.set('product_id', str(product.source_code))
                _modif.set('country_id', str(product.country.pk))
                if product.manufacturer:
                    _modif.set('manufacturer_id', str(product.manufacturer.pk))
                _modif.set('type', product.type)
                if product.white_brand:
                    _modif.set('wb_id', str(product.white_brand.pk))
                    _modif.set('wb_key', product.white_brand.factor_specific_key)
                    #_modif.set('wb_unit',product.white_brand.factor_specific_unit)
                    _modif.set('wb_value', str(product.factor_specific_value))


            structureXml = open(user_path + 'new.xml', 'w')#pr_name.text +'.xml', "w")
            structureXml.write(etree.tostring(NNPL, pretty_print=True, encoding="cp1251", xml_declaration=True))
            structureXml.close()
            print 'salepoints count ' + str(k)
            print 'offer count ' + str(of_count)
            ofile.close()
            afile.close()
            self.stdout.write('Successfully generated xml ')
        except Exception as e:
            raise CommandError('Some error detected: "%s" ' % str(e))


        '''
    data = []
    _new_products = Product.objects.filter(is_new=True)
    for pr in _new_products:
        el = {'product': {'title' : pr.title, 'title_extra' : pr.title_extra, 'manufacturer' : pr.manufacturer, 'wb_id' : pr.white_brand.ext_id}}
        offers = Offers.objects.filter(source_code=pr.source_code, source_type=pr.source_type)
        el['offers'] = {'offers': [{'price' : off.price, 'salepoint_id': off.salepoint.id}  for off in offers]}
        data.append(el)

    new_offers_products = simplejson.dumps(data)
    '''


