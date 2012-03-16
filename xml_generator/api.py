__author__ = 'eugene'
# -*- coding: utf-8 -*-
from tastypie import fields
from tastypie.resources import ModelResource
from models import *

from django.contrib.auth.models import User

class SalepointResource(ModelResource):
    #related_name  : helps to populate reverse relations; must be a field on the other Resource
    #full=True чтобы видеть начинку offers, а не просто их resource_uri
    #offers = fields.ToManyField('xml_generator.api.OfferResource','offer_set', related_name='salepoint', full=True)
    class Meta:
        queryset = Salepoint.objects.all()
        resource_name = 'salepoint'



class OfferResource(ModelResource):
    #salepoint = fields.ToOneField(SalepointResource, 'salepoint')
    class Meta:
        queryset = Offer.objects.all()
        resource_name = 'offer'

    def dehydrate(self, bundle):
        bundle.data['salepoint_id'] = bundle.obj.salepoint.id
        bundle.data['source_code'] = bundle.obj.product.source_code
        bundle.data['source_type'] = bundle.obj.product.source_type
        return bundle

