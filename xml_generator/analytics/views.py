# -*- coding: utf-8 -*
import json
import simplejson
from django.template import RequestContext
from django.shortcuts import render_to_response
from xml_generator.models import *
from django.db import connections
from django.db.models import Count
import datetime
from dateutil.relativedelta import relativedelta
from pyofc2  import * 
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.core.serializers.json import DjangoJSONEncoder

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


def product_anal(request, product_pk):
    sp_pk = request.GET.get('sp_pk', None)
    if sp_pk:
        sp = Salepoint.objects.get(pk=sp_pk)
    else:
        sp = Salepoint.objects.filter(offer__product__pk=product_pk).order_by('name')[0]
    pr = Product.objects.get(pk=product_pk)
    template = 'templates/product_analyt.html'
    context ={'product_id': product_pk, 'salepoint' : sp, 'current_product': pr,}
    return TemplateResponse(request, template, context)


def product_list_salepoint(request, product_pk):

    list_salepoint = Salepoint.objects.filter(offer__product__pk=product_pk).order_by('name')
    _list = []
    for sp in list_salepoint:
        _list.append({
            'sp_pk' : sp.pk,
            'sp_info': sp.name + ' ' + sp.address,
        })
    try:
        response = {
            'status' : 'OK',
            'list_salepoint' : _list,
            }

        content = simplejson.dumps(response)
        return HttpResponse(content, mimetype='application/javascript')
    except Exception as e:
        print str(e)
        response = {
            'status' : 'Error',
            'message' : str(e),
            }
        content = simplejson.dumps(response)
        return HttpResponse(content, mimetype='application/javascript')


def product_chart(request, product_pk, salepoint_pk):

    offs = Offer.all_objects.filter(product__pk=product_pk, salepoint__pk=salepoint_pk).order_by('created')

    _list = []
    for _offer in offs:
        _list.append({
            'created' : json.dumps(_offer.created, cls=DjangoJSONEncoder),
            'year' : _offer.created.year,
            'month' : _offer.created.month,
            'day' : _offer.created.day,
            'price': _offer.price,
            })
    try:
        response = {
            'status' : 'OK',
            'offers' : _list,
            }

        content = simplejson.dumps(response)
        return HttpResponse(content, mimetype='application/javascript')
    except Exception as e:
        print str(e)
        response = {
            'status' : 'Error',
            'message' : str(e),
            }
        content = simplejson.dumps(response)
        return HttpResponse(content, mimetype='application/javascript')