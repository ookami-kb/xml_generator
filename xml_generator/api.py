# -*- coding: utf-8 -*-
from tastypie import fields
from tastypie.resources import ModelResource, ALL
from models import *
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import BasicAuthentication
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import datetime
import time

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


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        filtering = {
                'username': ALL,
                }

class SalepointResource(ModelResource):
    def obj_create(self, bundle, request=None, **kwargs):
        return super(SalepointResource, self).obj_create(bundle, request, user=request.user)
    
    def hydrate(self, bundle):
        try:
            bundle.obj.id = int(bundle.data['salepoint_id'])
        except:
            pass
        
        # если мы изменяем уже существующую торговую точку, то не надо
        # менять ее организацию
        try:
            salepoint = Salepoint.objects.get(pk=bundle.obj.id)
            bundle.obj.organ = salepoint.organ
            # нахрен удаляем все офферы, относящиеся к данной торговой точке,
            # следующим этапом мы их все равно будем вносить
            Offer.objects.filter(salepoint=salepoint).delete()
        except Salepoint.DoesNotExist:
            # если мы создаем новую точку (бывает для заправок),
            # то можем попытаться присвоить ей организацию,
            # если юзер правильно ввел название
            try:
                bundle.obj.organ = Organization.objects.get(name=bundle.data['org'])
            except:
                bundle.obj.organ = Organization.objects.get(name='unknown')
        
        try:
            _coords = bundle.data['coords']
            bundle.obj.longitude = float(_coords.split(',')[1])
            bundle.obj.latitude = float(_coords.split(',')[0])
        except:
            pass
        return bundle

    def dehydrate(self, bundle):
        bundle.data['org'] = bundle.obj.organ.name
        if bundle.obj.longitude is not None  and bundle.obj.latitude is not None:
            bundle.data['coords'] = unicode(bundle.obj.latitude) + u',' + unicode(bundle.obj.longitude)
        return bundle

    def get_object_list(self, request, *args, **kwargs):
        return Salepoint.objects.filter(user=request.user)

    class Meta:
        queryset = Salepoint.objects.all()
        resource_name = 'salepoint'
        authentication = MyAuthentication()
        authorization = DjangoAuthorization()



class OfferResource(ModelResource):
    class Meta:
        queryset = Offer.objects.all()
        resource_name = 'offer'
        authentication = MyAuthentication()
        authorization = DjangoAuthorization()

    def dehydrate(self, bundle):
        bundle.data['salepoint_id'] = bundle.obj.salepoint.id
        bundle.data['source_code'] = bundle.obj.product.source_code
        bundle.data['source_type'] = bundle.obj.product.source_type
        bundle.data['title'] = bundle.obj.product.title
        try:
            bundle.date['timestamp'] = time.mktime(bundle.obj.created.timetuple())
        except:
            pass
        return bundle

    def hydrate(self, bundle):
        try:
            bundle.obj.created = datetime.date.fromtimestamp(int(bundle.data['timestamp']))
        except:
            bundle.obj.created = datetime.datetime.now()
        bundle.obj.salepoint = Salepoint.objects.get(pk=bundle.data['salepoint_id'])
        bundle.obj.product = Product.objects.get(source_code=bundle.data['source_code'],
                                                 source_type=bundle.data['source_type'])
        return bundle

    def get_object_list(self, request, *args, **kwargs):
        return Offer.objects.filter(salepoint__user=request.user)

class ProductResource(ModelResource):
    class Meta:
        queryset = Product.objects.all()
        resource_name = 'product'
        authorization = DjangoAuthorization()
        authentication = MyAuthentication()

    def hydrate(self, bundle):
        bundle.obj.white_brand = WhiteBrand.objects.get(pk=bundle.data['white_brand'])
        return bundle