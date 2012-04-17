__author__ = 'eugene'
# -*- coding: utf-8 -*-
from xml_generator.models import *
from django.core.management.base import BaseCommand, CommandError




class Command(BaseCommand):
    args = ''
    help = 'set salepoint variation'


    def handle(self, *args, **options):
        try:
            sps = Salepoint.objects.all()
            for sp in sps:
                ofs = Offer.objects.filter(salepoint=sp)
                contains_fuel = False
                for of in ofs:
                    if of.product.type == u'fuel':
                        contains_fuel = True
                if contains_fuel:
                    sp.variation = u'fuel'
                else:
                    sp.variation = u'product'
                sp.save()


        except Exception as e:
            raise CommandError('Some error detected: "%s" ' % str(e))