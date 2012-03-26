# -*- coding: utf-8 -*
from django.contrib import admin
from .models import *

admin.site.register(WhiteBrand)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_extra', 'manufacturer', 'white_brand',
              'source_code', 'source_type', 'is_new')
    list_filter = ('is_new',)
    
admin.site.register(Product, ProductAdmin)

class OfferAdmin(admin.ModelAdmin):
    list_display = ('product', 'salepoint', 'price', 'created')
    
admin.site.register(Offer, OfferAdmin)

class SalepointAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'organ', 'user', 'city')
    list_filter = ('organ', 'user')
    
admin.site.register(Salepoint, SalepointAdmin)

admin.site.register(Organization)