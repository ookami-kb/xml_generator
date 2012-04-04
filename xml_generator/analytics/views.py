# -*- coding: utf-8 -*
from django.template import RequestContext
from django.shortcuts import render_to_response
from xml_generator.models import Offer
from django.db import connections
from django.db.models import Count
import datetime
from dateutil.relativedelta import relativedelta
from pyofc2  import * 
from django.http import HttpResponse

def generate_days():
    cur = datetime.date.today().replace(day=1)
    d = {}
    step = datetime.timedelta(days=1)
    till_date = cur + relativedelta(months=+1)
    while cur < till_date:
        d[cur.strftime('%Y-%m-%d %H:%M:%S')] = 0
        cur += step
    return d

def offers(request):
    return render_to_response('analytics/offers.djhtml', {}, RequestContext(request))

def offers_data(request):
    days = Offer.objects.all().extra(select={'day': connections[Offer.objects.db]\
        .ops.date_trunc_sql('day', 'created')})\
        .values('day').annotate(qty=Count('price')).order_by('-day')
        
    data = generate_days()
    for day in days:
        data[day['day']] = day['qty']
    sorted_data = [{'day': k, 'qty': data[k]} for k in sorted(data)]
    
    t = title(text=u"Кол-во предложений в текущем месяце")
    s = line()
    s.values = [k['qty'] for k in sorted_data]
    
    xa = x_axis()
    
    xlbls = x_axis_labels()

    lbls = [datetime.datetime.strptime(k['day'], '%Y-%m-%d %H:%M:%S').strftime('%d') for k in sorted_data]
    xlbls.labels = lbls
    xa.labels = xlbls
    
    chart = open_flash_chart()
    chart.x_axis = xa
    
    ya = y_axis()
    ya.min = min(s.values)
    ya.max = max(s.values)
    
    chart.y_axis = ya
    
    chart.title = t    
    chart.add_element(s)
    return HttpResponse(chart.render())
    