# -*- coding: utf-8 -*
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from xml_generator.models import Salepoint
import datetime
from django.db.models import Count

from .forms import DateRange

@staff_member_required
def salepoints_stat(request):
    date_range = DateRange(request.GET)
    if date_range.is_valid():
        start = date_range.cleaned_data['start']
        stop = date_range.cleaned_data['stop']
    else:
        start = None
        stop = None
        
    filters = {}
    salepoints = Salepoint.objects.all()
    if start:
        filters['offer__created__gte'] = start
    if stop:
        filters['offer__created__lte'] = stop + datetime.timedelta(days=1)
    
    if filters:
        salepoints = salepoints.filter(**filters)
        
    salepoints = salepoints.annotate(offers_count=Count('offer'))\
            .filter(offers_count__gt=0)
    return render_to_response(
        "admin/salepoints_stat.djhtml",
        {'salepoints' : salepoints,
         'date_range': date_range},
        RequestContext(request, {}),
    )