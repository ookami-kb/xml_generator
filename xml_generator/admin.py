# -*- coding: utf-8 -*
from django.contrib import admin
from .models import *
from django import forms
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotFound
from django.template import RequestContext, loader
from django.shortcuts import render

admin.site.register(WhiteBrand)

class ModerateProductForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    product = forms.ModelChoiceField(queryset=Product.objects.filter(is_new=False), label=u'Старые продукты')

def moderate_product(modeladmin, request, queryset):
    form = None
    if 'apply' in request.POST:
        form = ModerateProductForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']

            cunt = 0
            for item in queryset:
                item.product_moderated = product
                item.save()
                cunt += 1

            modeladmin.message_user(request, "Старый продукт %s привязан к %d новым продуктам." % (product, cunt))
            return HttpResponseRedirect(request.get_full_path())
    if not form:
        form = ModerateProductForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

    return render(request, 'templates/moderate_product.html', {'items': queryset,'form': form, 'title':u'Привязка к существующему продукту'})

moderate_product.short_description = u"Привязать к продукту"


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_extra', 'manufacturer', 'white_brand',
              'source_code', 'source_type', 'is_new')
    list_filter = ('is_new',)
    actions = [moderate_product,]
    
admin.site.register(Product, ProductAdmin)

class OfferAdmin(admin.ModelAdmin):
    list_display = ('product', 'salepoint', 'price', 'created')
    
admin.site.register(Offer, OfferAdmin)

class SalepointAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'organ', 'user', 'city')
    list_filter = ('organ', 'user', 'is_new')
    
admin.site.register(Salepoint, SalepointAdmin)

admin.site.register(Organization)