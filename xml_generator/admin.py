# -*- coding: utf-8 -*
from django.contrib import admin
from .models import WhiteBrand, Product, Offer, Salepoint

admin.site.register(WhiteBrand)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_extra', 'manufacturer', 'white_brand',
              'source_code', 'source_type', 'is_new')
    
admin.site.register(Product, ProductAdmin)

class OfferAdmin(admin.ModelAdmin):
    list_display = ('product', 'salepoint', 'price')
    
admin.site.register(Offer, OfferAdmin)

class SalepointAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    
admin.site.register(Salepoint, SalepointAdmin)