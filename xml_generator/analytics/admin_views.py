# -*- coding: utf-8 -*
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from xml_generator.models import Salepoint, Offer
import datetime
from django.db.models import Count
from django.contrib.auth.models import User

from .forms import DateRange, UserSelect

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
        
    filters = {}
    offers = Offer.objects.all()
    if start:
        filters['created__gte'] = start
    if stop:
        filters['created__lte'] = stop + datetime.timedelta(days=1)
    if uid:
        filters['salepoint__user__id'] = uid
    
    if filters:
        offers = offers.filter(**filters)
        
    offers = offers.values('salepoint__user', 'salepoint__id', 'salepoint__name', 'created').annotate(offers_count=Count('id'))
    
    print offers
        
    return render_to_response(
        "admin/salepoints_stat.djhtml",
        {'offers' : offers,
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
        
    users = User.objects.all()
    
    # кол-во загруженных предложений в заданном промежутке
    users = users.extra(select={'offers_count': 'SELECT COUNT(*) FROM xml_generator_offer WHERE xml_generator_offer.salepoint_id IN (SELECT DISTINCT id from xml_generator_salepoint WHERE xml_generator_salepoint.user_id = auth_user.id) AND xml_generator_offer.created >= %s and xml_generator_offer.created <= %s'},
                        select_params=(start, stop))
    
    # кол-во мониторенных магазинов в заданном промежутке
    users = users.extra(select={'salepoints_count': 'SELECT COUNT(*) FROM (SELECT * FROM xml_generator_offer WHERE xml_generator_offer.salepoint_id IN (SELECT id from xml_generator_salepoint WHERE xml_generator_salepoint.user_id = auth_user.id) AND xml_generator_offer.created >= %s and xml_generator_offer.created <= %s GROUP BY xml_generator_offer.salepoint_id, xml_generator_offer.created)'},
                        select_params=(start, stop))
    
    print users.query
    
    # выбираем кол-во предложений, которые пользователи загрузили
    # в заданном промежутке
#    users = users.annotate(offers_count=Count)

    return render_to_response(
        "admin/users_stat.djhtml",
        {'users' : users,
         'date_range': date_range},
        RequestContext(request, {}),
    )