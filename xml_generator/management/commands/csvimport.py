# -*- coding: utf-8 -*-
'''
Created on 27.04.2012

@author: gorodechnyj
'''

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction 
from xml_generator.models import Offer, Product
from optparse import make_option
import csv

class CSV2Offer(object):
    def __init__(self, filename):
        self.file = open(filename, 'rb')
        self.salepoints = []
        
    def process(self):
        try:
            reader = csv.reader(self.file, dialect='excel', delimiter=',')
        except Exception, e:
            raise Exception(u"Ошибка при проверке файла: %s" % e)
        for row_index, row in enumerate(reader):
            if row_index == 0:
                self.prepare_salepoints(row)
            else:
                self.parse_row(row)
        self.file.close()

    @transaction.commit_on_success
    def prepare_salepoints(self, row):
        for sp in row[1:]:
            try:
                sp = int(sp)
            except ValueError:
                raise Exception(u'Не валидный идентификатор прайс-листа: %s' % sp)
            Offer.objects.filter(salepoint__id=sp).update(is_redundant=True)
            self.salepoints.append(sp)

    def save_prices(self, prices, product):
        for index, salepoint in enumerate(self.salepoints):
            try:
                price = float(prices[index])
            except:
                continue
            offer = Offer(price = price,
                          salepoint_id = salepoint, 
                          product = product,
                          is_redundant = False)
            offer.save(force_insert=True)
    
    def parse_row(self, row):
        source_code = row[0]
        # prices
        prices = row[1:]
        # get modification
        try:
            product = Product.objects.get(source_code = source_code)
            #insert prices
            self.save_prices(prices, product)
        except Product.DoesNotExist:
            print u'Product with source code %s does not exists' % source_code
            pass
        
        


class Command(BaseCommand):
    help = 'Import offers from csv'
    option_list = BaseCommand.option_list + (
        make_option('-i','--import file',
            action='store',
            type='string',
            dest = 'filename',
            default='',
            help='CSV import file'
        ),
    )
    
    def handle(self, *args, **options):
        if not options['filename']:
            raise CommandError('You need to specify import file')
        processor = CSV2Offer(options['filename'])
        processor.process()
