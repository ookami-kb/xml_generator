# -*- coding: utf-8 -*
from django.db import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth.models import User

class WhiteBrand(models.Model):
    name = models.CharField(verbose_name=u'Название', max_length=30)
    ext_id = models.IntegerField(verbose_name=u'Ключ Neiron',
                                 help_text=u'PK бренда в системе Neiron',
                                 primary_key=True)
    
    def __unicode__(self):
        return self.name
    
class Product(models.Model):
    title = models.CharField(verbose_name=u'Название', max_length=255)
    title_extra = models.CharField(u'Доп. название', max_length=255)
    source_code = models.IntegerField()
    source_type = models.CharField(max_length=255)
    manufacturer = models.CharField(u'Производитель', max_length=255)
    white_brand = models.ForeignKey(WhiteBrand)
    is_new = models.BooleanField(u'Новый', help_text='Этот продукт был создан пользователем и еще не прошел модерацию')
    
    def __unicode__(self):
        return u'%s. %s' % (self.title, self.title_extra)
    
    def clean(self):
        # надо удостовериться, что есть только один продукт с таким
        # source_code и source_type
        if Product.objects.filter(source_code=self.source_code, 
                                  source_type=self.source_type).exclude(pk=self.pk).count():
            raise ValidationError('Продукт с такими source_type/source_code уже существует')


    def save(self, *args, **kwargs):
        try:
            self.pk = Product.objects.get(source_code=self.source_code, source_type=self.source_type).pk
        except:
            self.pk = None
        #pr =  self.logic()
        return super(Product, self).save(*args, **kwargs)
    
class Salepoint(models.Model):
    name = models.CharField(u'Название', max_length=255)
    address = models.CharField(u'Адрес', max_length=255)
    latitude = models.FloatField(u'Широта', null=True, blank=True)
    longitude = models.FloatField(u'Долгота', null=True, blank=True)
    organ     = models.CharField(u'Организация', max_length=255)
    user = models.ForeignKey(User)

    
    def __unicode__(self):
        return u'%s, %s' % (self.name, self.address)
    
class Offer(models.Model):
    product = models.ForeignKey(Product)
    salepoint = models.ForeignKey(Salepoint)
    price = models.FloatField(u'Цена')
    
    def __unicode__(self):
        return u'%s в магазине %s' % (self.product, self.salepoint)
    