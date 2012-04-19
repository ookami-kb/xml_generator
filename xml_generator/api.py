# -*- coding: utf-8 -*-
from tastypie import fields
from tastypie.resources import ModelResource, ALL
from models import *
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.authentication import BasicAuthentication
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Q
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


class WhiteBrandResource(ModelResource):
    class Meta:
        queryset = WhiteBrand.objects.all().order_by('pk')
        authentication = MyAuthentication()
        authorization = DjangoAuthorization()
        resource_name = 'whitebrand'

class SalepointResource(ModelResource):
    def obj_create(self, bundle, request=None, **kwargs):
        return super(SalepointResource, self).obj_create(bundle, request, user=request.user)

    def dispatch(self, request_type, request, **kwargs):
        '''
        tasks = Task.objects.filter(user=request.user, date_to_execute__day=datetime.datetime.now().day)
        self.sp_list = []
        for task in tasks:
            _l = []
            for sp in task.salepoint.filter(is_new=False, is_redundant=False):
                _l.append(sp.pk)
            self.sp_list.append({task.pk : _l})
            '''
        self.sp_list = []
        try:
            task = Task.objects.get(user=request.user, date_to_execute__day=datetime.datetime.now().day)
            self.task_pk = task.pk
            for sp in task.salepoint.filter(is_new=False, is_redundant=False):
                self.sp_list.append(sp.pk)
        except:
            pass

        return super(SalepointResource, self).dispatch(request_type, request, **kwargs)

    def hydrate(self, bundle):
        try:
            bundle.obj.id = int(bundle.data['salepoint_id'])
            #пришелоффер на точку --- удаляем ее изс писка, удалили все тп --- зад ание выполнено
            self.sp_list.remove(bundle.obj.id)
            if len(self.sp_list) == 0:
                his_task = Task.objects.get(pk=self.task_pk)
                his_task.accomplished = True
                his_task.save()


        except:
            pass
        
        try:
            _coords = bundle.data['coords']
            bundle.obj.longitude = float(_coords.split(',')[1])
            bundle.obj.latitude = float(_coords.split(',')[0])
        except:
            pass

        bundle.obj.is_new = True
        bundle.obj.is_redundant=False
        bundle.obj.last_modified_time = datetime.datetime.now()
        try:
            bundle.obj.user = User.objects.get(username=bundle.data['username'])
        except:
            bundle.obj.user = None
        return bundle

    def dehydrate(self, bundle):
        bundle.data['org'] = bundle.obj.organ.name
        if bundle.obj.longitude is not None  and bundle.obj.latitude is not None:
            bundle.data['coords'] = unicode(bundle.obj.latitude) + u',' + unicode(bundle.obj.longitude)
        return bundle

    #def get_object_list(self, request, *args, **kwargs):
    #    return Salepoint.objects.filter(((Q(user=request.user) & Q(is_new=True)) & Q(is_redundant=False)) | (Q(user=request.user) & Q(is_new=False) & Q(is_redundant=False) ))
    def get_object_list(self, request, *args, **kwargs):
        tasks = Task.objects.filter(user=request.user, date_to_execute__day=datetime.datetime.now().day)
        sp_list = []
        for task in tasks:
            for sp in task.salepoint.filter(is_new=False, is_redundant=False):
                sp_list.append(sp.pk)

        return Salepoint.objects.filter(pk__in=sp_list)

    class Meta:
        queryset = Salepoint.objects.all().order_by('pk')
        resource_name = 'salepoint'
        authentication = MyAuthentication()
        authorization = DjangoAuthorization()


class FuelResource(ModelResource):
    class Meta:
        queryset = Offer.objects.all().order_by('pk')
        resource_name = 'fuel'
        authentication = MyAuthentication()
        authorization = DjangoAuthorization()

    def __init__(self, *args, **kwargs):
        super(FuelResource, self).__init__(*args, **kwargs)

    def dehydrate(self, bundle):
        bundle.data['salepoint_id'] = bundle.obj.salepoint.id
        bundle.data['source_code'] = bundle.obj.product.source_code
        bundle.data['source_type'] = bundle.obj.product.source_type
        bundle.data['title'] = bundle.obj.product.title
        try:
            bundle.data['timestamp'] = time.mktime(bundle.obj.created.timetuple())
        except:
            pass
        return bundle

    def get_object_list(self, request, *args, **kwargs):
        return Offer.objects.filter(salepoint__user=request.user, product__type=u'fuel')

class OfferResource(ModelResource):
    class Meta:
        queryset = Offer.objects.all().order_by('pk')
        resource_name = 'offer'
        authentication = MyAuthentication()
        authorization = DjangoAuthorization()
        
    def __init__(self, *args, **kwargs):
        super(OfferResource, self).__init__(*args, **kwargs)
        self.trashed_sp = []
            
    def dehydrate(self, bundle):
        bundle.data['salepoint_id'] = bundle.obj.salepoint.id
        bundle.data['source_code'] = bundle.obj.product.source_code
        bundle.data['source_type'] = bundle.obj.product.source_type
        bundle.data['title'] = bundle.obj.product.title
        try:
            bundle.data['timestamp'] = time.mktime(bundle.obj.created.timetuple())
        except:
            pass
        return bundle



    def dispatch(self, request_type, request, **kwargs):
        self.created = datetime.datetime.now()
        return super(OfferResource, self).dispatch(request_type, request, **kwargs)

    def hydrate(self, bundle):
        try:
            user = User.objects.get(username=bundle.data['username'])
        except:
            user = None
            
        try:
            bundle.obj.created = datetime.date.fromtimestamp(int(bundle.data['timestamp']))
        except:
            bundle.obj.created = self.created
            
        salepoint = Salepoint.objects.get(pk=bundle.data['salepoint_id'])
        bundle.obj.salepoint = salepoint
        
        if salepoint not in self.trashed_sp:
            self.trashed_sp.append(salepoint)
            Offer.objects.filter(salepoint=salepoint).update(is_redundant=True)
            
        #если продукт отмодерирован и есть эталонный(другой), то предложение переназначается на него
        try:
            _pr = Product.objects.get(source_code=bundle.data['source_code'],
            source_type=bundle.data['source_type'])
            
            # если продукт помечен как удаленный, не сохраняем на него предложения
            if _pr.is_redundant:
                return None
        except:
            # если такого продукта нет, то создаем его
            _pr = Product(source_code=bundle.data['source_code'],
                          source_type=bundle.data['source_type'],
                          is_new=True,
                          country=Country.objects.get(name=u'Россия'),
                          white_brand=WhiteBrand.objects.get(pk=bundle.data['white_brand']) or None,
                          user=user,
                          title=bundle.data['title']
                          )
            _pr.save()
            
        bundle.obj.product = _pr
        if not _pr.is_new:
            if _pr.product_moderated:
                bundle.obj.product = _pr.product_moderated

        try:
            _sp = Salepoint.objects.get(pk=bundle.data['salepoint_id'], is_redundant=False)
        except:
            return None
        _sp.last_modified_time = datetime.datetime.now()

        return bundle

    def get_object_list(self, request, *args, **kwargs):
        return Offer.objects.filter(salepoint__user=request.user)

class ProductResource(ModelResource):
    class Meta:
        queryset = Product.objects.all().order_by('pk')
        excludes = ['id', 'is_new', 'is_redundant',]
        resource_name = 'product'
        authorization = DjangoAuthorization()
        authentication = MyAuthentication()

    def dehydrate(self, bundle):
        bundle.data['manufacturer'] = bundle.obj.manufacturer.name if bundle.obj.manufacturer else u''
        bundle.data['whitebrand_id'] = bundle.obj.white_brand.pk if  bundle.obj.white_brand else 0
        return bundle

    def hydrate(self, bundle):
        if int(bundle.data['white_brand']) == 0:
            bundle.obj.white_brand = None
        else:
            bundle.obj.white_brand = WhiteBrand.objects.get(pk=bundle.data['white_brand'])
        bundle.obj.is_new = True
        bundle.obj.is_redundant = False
        try:
            bundle.obj.user = User.objects.get(username=bundle.data['username'])
        except:
            bundle.obj.user = None

        bundle.obj.country = Country.objects.get(name=u'Россия')
        return bundle

    def get_object_list(self, request, *args, **kwargs):
        #Отмодерированные продукты выгружаются всем. Неотмодерированные - только создавшим их пользователям.
        return Product.objects.filter(((Q(user=request.user) & Q(is_new=True)) & Q(is_redundant=False)) | (Q(is_new=False) & Q(product_moderated=None) & Q(is_redundant=False) ))


class FuelProductResource(ModelResource):
    class Meta:
        queryset = Product.objects.all().order_by('pk')
        excludes = ['id', 'is_new', 'is_redundant',]
        resource_name = 'fuel_product'
        authorization = DjangoAuthorization()
        authentication = MyAuthentication()

    def dehydrate(self, bundle):
        bundle.data['manufacturer'] = bundle.obj.manufacturer.name if bundle.obj.manufacturer else u''
        bundle.data['whitebrand_id'] = bundle.obj.white_brand.pk if  bundle.obj.white_brand else 0
        return bundle

    def hydrate(self, bundle):
        if int(bundle.data['white_brand']) == 0:
            bundle.obj.white_brand = None
        else:
            bundle.obj.white_brand = WhiteBrand.objects.get(pk=bundle.data['white_brand'])
        bundle.obj.is_new = True
        bundle.obj.is_redundant = False
        try:
            bundle.obj.user = User.objects.get(username=bundle.data['username'])
        except:
            bundle.obj.user = None

        bundle.obj.country = Country.objects.get(name=u'Россия')
        return bundle

    def get_object_list(self, request, *args, **kwargs):
        #Отмодерированные продукты выгружаются всем. Неотмодерированные - только создавшим их пользователям.
        return Product.objects.filter((((Q(user=request.user) & Q(is_new=True)) & Q(is_redundant=False)) | (Q(is_new=False) & Q(product_moderated=None) & Q(is_redundant=False) ))&Q(type=u'fuel'))

