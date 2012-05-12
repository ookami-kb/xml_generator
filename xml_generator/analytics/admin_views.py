# -*- coding: utf-8 -*
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from xml_generator.models import *
import datetime
from django.db.models import Count
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import DateRange, UserSelect

def ValuesQuerySetToDict(vqs):
    return [item for item in vqs]

@staff_member_required
def salepoints_stat(request):
    users = UserSelect(request.GET)
    date_range = DateRange(request.GET)
    if date_range.is_valid():
        start = date_range.cleaned_data['start'] or datetime.date.fromtimestamp(0)
        stop = date_range.cleaned_data['stop'] or datetime.date.today() + datetime.timedelta(days=1)
    else:
        start = datetime.date.fromtimestamp(0)
        stop = datetime.date.today() + datetime.timedelta(days=1)
        
    if users.is_valid():
        uid = users.cleaned_data['user']
    else:
        uid = None
    _off = []
    if not uid:
        for uid in User.objects.exclude(username__in=['admin', 'fuel', 'test_fuel', 'test']):
            for t in Task.objects.filter(date_to_execute__gte=start, date_to_execute__lte=stop, is_pattern=False, user=uid):
                for sp in t.salepoint.all():
                    _o = Offer.objects.filter(created__gte=start, created__lte=stop, created__day=t.date_to_execute.day ,\
                        created__month=t.date_to_execute.month, created__year=t.date_to_execute.year,\
                        salepoint=sp).select_related()
                    #for o in _o:
                    #    print o.created
                    # print  '\n !  '
                    _count = _o.count()
                    #print _count
                    # print _o
                    #_a = ValuesQuerySetToDict(_o)
                    #_o['offers_count'] = _count
                    _off.append({
                        'salepoint__user' : uid,
                        'salepoint__id' : sp.pk,
                        'salepoint__name' : sp.name,
                        'salepoint__address' : sp.address,
                        'created' : str(t.date_to_execute.day) + '.' + str(t.date_to_execute.month) + '.' + str(t.date_to_execute.year),
                        'offers_count' : _count,
                        })
    else:
        for t in Task.objects.filter(date_to_execute__gte=start, date_to_execute__lte=stop, is_pattern=False, user=uid):
            for sp in t.salepoint.all():
                _o = Offer.objects.filter(created__gte=start, created__lte=stop, created__day=t.date_to_execute.day ,\
                    created__month=t.date_to_execute.month, created__year=t.date_to_execute.year,\
                    salepoint=sp).select_related()
                #for o in _o:
                #    print o.created
               # print  '\n !  '
                _count = _o.count()
                #print _count
               # print _o
                #_a = ValuesQuerySetToDict(_o)
            #_o['offers_count'] = _count
                _off.append({
                    'salepoint__user' : uid,
                    'salepoint__id' : sp.pk,
                    'salepoint__name' : sp.name,
                    'salepoint__address' : sp.address,
                    'created' : str(t.date_to_execute.day) + '.' + str(t.date_to_execute.month) + '.' + str(t.date_to_execute.year),
                    'offers_count' : _count,
                })
            #print _off

    '''
    filters = {}
    offers = Offer.objects.all()
    if start:
        filters['created__gte'] = start
    if stop:
        filters['created__lte'] = stop + datetime.timedelta(days=1)
    if uid:
        filters['salepoint__user'] = uid
    
    if filters:
        offers = offers.filter(**filters)



    offers = offers.values('salepoint__user', 'salepoint__id', 'salepoint__name', 'created').annotate(offers_count=Count('id'))
    
    print offers
    '''
    return render_to_response(
        "admin/salepoints_stat.djhtml",
        {'offers' : _off,
         'date_range': date_range,
         'users_form': users},
        RequestContext(request, {}),
    )
    
@staff_member_required
def users_stat(request):
    date_range = DateRange(request.GET)
    if date_range.is_valid():
        start = date_range.cleaned_data['start'] or datetime.date.fromtimestamp(0)
        stop = date_range.cleaned_data['stop'] or datetime.date.today() + datetime.timedelta(days=1)
    else:
        start = datetime.date.fromtimestamp(0)
        stop = datetime.date.today() + datetime.timedelta(days=1)
        
    users = User.objects.exclude(username__in=['admin', 'fuel', 'test_fuel', 'test'])


    _users = []
    for u in users:
        # кол-во загруженных предложений в заданном промежутке
        _offer_count = 0
        # кол-во мониторенных магазинов в заданном промежутке
        _sp_count = 0
        '''
        for t in Task.objects.filter(Q(date_to_execute__gte=start) & Q(date_to_execute__lte=stop) & Q(is_pattern=False) & Q(user=u)):

            _offer_count +=  Offer.objects.filter(Q(created__gte=start) & Q(created__lte=stop) & Q(created__day=t.date_to_execute.day) &\
                                           Q(created__month=t.date_to_execute.month) & Q(created__year=t.date_to_execute.year) &\
                                            Q(salepoint__in=t.salepoint.all())).count()

            #if t.salepoint in
            _sp_count += t.salepoint.count()

        '''


        for t in Task.objects.filter(date_to_execute__gte=start, date_to_execute__lte=stop, is_pattern=False, user=u):


            _off = Offer.all_objects.filter(created__gte=start, created__lte=stop, created__day=t.date_to_execute.day , \
                                                  created__month=t.date_to_execute.month, created__year=t.date_to_execute.year,\
                                                    salepoint__in=t.salepoint.all())
            #print _off
            _offer_count += _off.count()
            #if t.salepoint in
            _sp_count += t.salepoint.count()
            #print t.user.username
        #print u.username + ' ' + str(u.pk) + ' ' + str(_offer_count) + ' ' + str(_sp_count) + '\n'

        _users.append({
            'user': u,
            'offers_count': _offer_count,
            'sps_count' : _sp_count,
        })
    #print users.query
    
    # выбираем кол-во предложений, которые пользователи загрузили
    # в заданном промежутке
#    users = users.annotate(offers_count=Count)

    return render_to_response(
        "admin/users_stat.djhtml",
        {'users' : _users,
         'date_range': date_range},
        RequestContext(request, {}),
    )