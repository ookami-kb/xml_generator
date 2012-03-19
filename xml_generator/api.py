# -*- coding: utf-8 -*-
from tastypie import fields
from tastypie.resources import ModelResource
from models import *
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.authentication import BasicAuthentication
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


class MyAuthentication(BasicAuthentication):
    def is_authenticated(self, request, **kwargs):
        _username = request.POST.get('username') or  request.GET.get('username')
        _password = request.POST.get('password') or  request.GET.get('password')
        user = authenticate(username=_username, password=_password)
        if user is not None:
            if user.is_active:
                login(request, user)
            else: return self._unauthorized()
        else: return self._unauthorized()


        return True


class SalepointResource(ModelResource):
    #related_name  : helps to populate reverse relations; must be a field on the other Resource
    #full=True чтобы видеть начинку offers, а не просто их resource_uri
    #offers = fields.ToManyField('xml_generator.api.OfferResource','offer_set', related_name='salepoint', full=True)

    def hydrate(self, bundle):
        bundle.obj.user = bundle.request.user

        try:
            bundle.obj.pk = int(bundle.data['salepoint_id'])
        except:
            pass

        try:
            _coords = bundle.data['coords']
            bundle.obj.longitude = float(_coords.split(',')[1])
            bundle.obj.latitude = float(_coords.split(',')[0])
        except:
            pass
        return bundle

    def dehydrate(self, bundle):
        if bundle.obj.longitude is not None  and bundle.obj.latitude is not None:
            bundle.data['coords'] = unicode(bundle.obj.latitude) + u',' + unicode(bundle.obj.longitude)
        return bundle

    class Meta:
        queryset = Salepoint.objects.all()
        resource_name = 'salepoint'
        authentication = MyAuthentication()



class OfferResource(ModelResource):
    #salepoint = fields.ToOneField(SalepointResource, 'salepoint')
    class Meta:
        queryset = Offer.objects.all()
        resource_name = 'offer'
        #authorization = Authorization()
        authentication = MyAuthentication()

    def dehydrate(self, bundle):
        bundle.data['salepoint_id'] = bundle.obj.salepoint.id
        bundle.data['source_code'] = bundle.obj.product.source_code
        bundle.data['source_type'] = bundle.obj.product.source_type
        return bundle

    def hydrate(self, bundle):
        bundle.obj.salepoint = Salepoint.objects.get(pk=bundle.data['salepoint_id'])
        bundle.obj.product = Product.objects.get(pk=bundle.data['product_id'])
        return bundle



class ProductResource(ModelResource):
    class Meta:
        queryset = Product.objects.all()
        resource_name = 'product'
        #authorization = Authorization()
        authentication = MyAuthentication()

    def hydrate(self, bundle):
        bundle.obj.white_brand = WhiteBrand.objects.get(pk=bundle.data['white_brand'])
        return bundle