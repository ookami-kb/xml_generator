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

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_extra', 'manufacturer', 'white_brand',
              'source_code', 'source_type', 'is_new', 'country', 'is_redundant')
    list_filter = ('is_new', 'user', 'is_redundant',)
    actions = [moderate_product,]
    
admin.site.register(Product, ProductAdmin)

class OfferAdmin(admin.ModelAdmin):
    list_display = ('product', 'salepoint', 'price', 'created', 'is_redundant')
    list_filter = ('product__is_new','salepoint__user', 'salepoint')

admin.site.register(Offer, OfferAdmin)

class SalepointAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'organ', 'last_modified_time', 'user', 'city', 'is_new', 'is_redundant')
    list_filter = ('user', 'is_new','user', 'is_redundant','organ', )
    actions = [moderate_salepoint, ]

    
admin.site.register(Salepoint, SalepointAdmin)

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk',)


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Country)
admin.site.register(Manufacturer)

class MyUserAdmin(UserAdmin):
    list_filter = UserAdmin.list_filter + ('salepoint',)

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)