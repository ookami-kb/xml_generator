# -*- coding: utf-8 -*
from django.contrib import admin
from .models import *
from django import forms
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotFound
from django.template import RequestContext, loader
from django.shortcuts import render
from datetime import datetime
import time
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.register(WhiteBrand)

class ModerateProductForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    product = forms.ModelChoiceField(queryset=Product.objects.filter(is_new=False), label=u'продукт')

class CreateNewProductForm(forms.ModelForm):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    class Meta:
        model = Product
        exclude=('source_code','is_redundant','is_new','product_moderated','source_type',)

def moderate_product(modeladmin, request, queryset):
    form = None
    form_create_new = None
    if 'apply' in request.POST:
        form = ModerateProductForm(request.POST)
        form_create_new = CreateNewProductForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            cunt = 0
            for item in queryset:
                item.product_moderated = product
                item.is_new = False
                item.save()
                cunt += 1
            modeladmin.message_user(request, "Старый продукт из базы данных %s привязан к %d новым продуктам от сборщиков." % (product, cunt))
            return HttpResponseRedirect(request.get_full_path())
        elif form_create_new.is_valid():
            new_product = form_create_new.save(commit=False)
            new_product.product_moderated=None
            new_product.source_code = int(time.time())
            new_product.is_redundant=False
            new_product.is_new=False
            new_product.source_type="new"
            new_product.save()
            cunt = 0
            for item in queryset:
                item.product_moderated = new_product
                item.is_new = False
                item.save()
                cunt += 1
            modeladmin.message_user(request, "Создан новый эталанной продукт %s и привязан к %d новым продуктам от сборщиков." % (new_product, cunt))
            return HttpResponseRedirect(request.get_full_path())
    if not form and not form_create_new:
        form = ModerateProductForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
        form_create_new = CreateNewProductForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

    return render(request, 'templates/moderate_product.html', {'items': queryset,'form': form, 'form_create_new':form_create_new, 'title':u'Привязка к существующему продукту'})

moderate_product.short_description = u"Привязать новые продукты от сброщиков к имеющемуся продукту в базе данных или создать его"
'''
class ModerateSalepointForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    salepoint = forms.ModelChoiceField(queryset=Salepoint.objects.filter(is_new=False), label=u'точку продаж')

class CreateNewSalepointForm(forms.ModelForm):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    class Meta:
        model = Salepoint
        exclude=('last_modified_time','is_redundant','is_new','salepoint_moderated',)


def moderate_salepoint(modeladmin, request, queryset):
    form = None
    form_create_new = None
    if 'apply' in request.POST:
        form = ModerateSalepointForm(request.POST)
        form_create_new = CreateNewSalepointForm(request.POST)
        if form.is_valid():
            salepoint = form.cleaned_data['salepoint']

            cunt = 0
            for item in queryset:
                item.salepoint_moderated = salepoint
                item.is_new = False
                item.save()
                cunt += 1

            modeladmin.message_user(request, "Старая точка продаж из базы данных %s привязана к %d новым точкам продаж от сборщиков." % (salepoint, cunt))
            return HttpResponseRedirect(request.get_full_path())
        elif form_create_new.is_valid():
            new_salepoint = form_create_new.save(commit=False)
            new_salepoint.last_modified_date = datetime.now()
            new_salepoint.is_redundant = False
            new_salepoint.is_new = False
            new_salepoint.save()
            cunt = 0
            for item in queryset:
                item.salepoint_moderated = new_salepoint
                item.is_new = False
                item.save()
                cunt += 1
            modeladmin.message_user(request, "Создана новая эталанная точка продаж %s и привязана к %d новым точкам продаж от сборщиков." % (new_salepoint, cunt))
            return HttpResponseRedirect(request.get_full_path())
    if not form and not form_create_new:
        form = ModerateSalepointForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
        form_create_new = CreateNewSalepointForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

    return render(request, 'templates/moderate_salepoint.html', {'items': queryset,'form': form, 'form_create_new':form_create_new, 'title':u'Привязка к существующей точке продаж'})

moderate_salepoint.short_description = u"Привязать новые точки продаж от сборщиков к имеющейся точке продаж в базе данных или создать ее"
'''



class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_extra', 'manufacturer', 'white_brand', 'is_new', 'sort_weight')
    list_filter = ('white_brand', 'is_new', 'user', )
    actions = [moderate_product,]
    list_editable = [
        'sort_weight',
        ]
    
admin.site.register(Product, ProductAdmin)
class SelectRelatedModelAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if 'queryset' in kwargs:
            kwargs['queryset'] = kwargs['queryset'].select_related()
        else:
            db = kwargs.pop('using', None)
            kwargs['queryset'] = db_field.rel.to._default_manager.using(db).complex_filter(db_field.rel.limit_choices_to).select_related()
        return super(SelectRelatedModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class OfferAdmin(admin.ModelAdmin):
    list_display = ('product', 'salepoint', 'price', 'created')
    #list_filter = ('product__is_new','salepoint__user')
    search_fields = ['product__title','product__title_extra','salepoint__name', 'salepoint__address']
    list_select_related = True
    date_hierarchy = 'created'

admin.site.register(Offer, OfferAdmin)

from widgets import GoogleMapsWidget
class SalepointForm(forms.ModelForm):
    latitude = forms.CharField(label=u'Координаты', widget = GoogleMapsWidget(
        attrs={'width': 800, 'height': 400, 'longitude_id':'id_longitude'}),
        error_messages={'required': 'Please select point from the map.'})
    longitude = forms.CharField(widget = forms.HiddenInput())



class SalepointAdmin(admin.ModelAdmin):
    form = SalepointForm
    list_display = ('id', 'name', 'address', 'organ', 'last_modified_time', 'user', 'is_new', 'is_redundant', 'offers_count')
    list_filter = ('user', 'is_new', 'is_redundant',)
    search_fields = ['name', 'address', 'organ__name']
    list_select_related = True
    #actions = [moderate_salepoint, ]

    
admin.site.register(Salepoint, SalepointAdmin)


class SimpleLogsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'log_level', 'created', 'origin', 'target', 'user', )
    list_filter = ('user', 'origin',)
    list_select_related = True
    #actions = [moderate_salepoint, ]


admin.site.register(Simple_Logs, SimpleLogsAdmin)


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', )


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Country)
admin.site.register(Manufacturer)

class MyUserAdmin(UserAdmin):
    list_filter = UserAdmin.list_filter + ('salepoint','salepoint__user__username',)

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)

_d = {0 : u'понед',
      1 : u'втор',
      2 : u'среда',
      3 : u'четв',
      4 : u'пятн',
      5 : u'суб',
      6 : u'воскр',}

import datetime
class TaskAdmin(admin.ModelAdmin):
    filter_horizontal = ('salepoint',)
    def week_day_(self, obj):
        #return obj.date_to_execute.strftime('%a')
        return _d[obj.date_to_execute.weekday()]
    def date_to_execute_(self, obj):
        if not obj.is_pattern:
            return obj.date_to_execute
        else:
            return '----'
    week_day_.short_description = 'День недели'
    date_to_execute_.short_description = 'Дата исполнения'
    list_display = ('pk','user', 'week_day_', 'date_to_execute_', 'is_pattern')
    list_filter = ('user', 'is_pattern')
    date_hierarchy = 'date_to_execute'



    class Media:
        css = {
            "all": ("brrr.css",)
        }

admin.site.register(Task, TaskAdmin)