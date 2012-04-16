__author__ = 'eugene'
# -*- coding: utf-8 -*-
from xml_generator.models import *
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = ''
    help = 'remove all offers'


    def handle(self, *args, **options):
        try:
            Offer.objects.all().delete()
            Product.objects.all().delete()
            Salepoint.objects.all().delete()
            Organization.objects.all().delete()
            Manufacturer.objects.all().delete()
            Country.objects.all().delete()
            WhiteBrand.objects.all().delete()

        except Exception as e:
            raise CommandError('Some error detected: "%s" ' % str(e))

