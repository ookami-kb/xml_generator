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
    title_extra = models.CharField(u'Доп. название', max_length=255, blank=True, null=True)
    source_code = models.IntegerField()
    source_type = models.CharField(max_length=255)
    manufacturer = models.CharField(u'Производитель', max_length=255, blank=True, null=True)
    white_brand = models.ForeignKey(WhiteBrand, blank=True, null=True)
    is_new = models.BooleanField(u'Новый', help_text='Этот продукт был создан пользователем и еще не прошел модерацию')
    
    def __unicode__(self):
        return u'%s. %s (%s)' % (self.title, self.title_extra, self.manufacturer)
    
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


class Organization(models.Model):
    name = models.CharField(verbose_name=u'Название', max_length=300)
    ext_id = models.IntegerField(verbose_name=u'Ключ Neiron',
        help_text=u'PK организации в системе Neiron',
        primary_key=True)

    def __unicode__(self):
        return self.name


class Salepoint(models.Model):
    POINT_TYPE = (
        (u"salon", u"Магазин-салон"),
        (u"release", u"Пункт выдачи товара"),
        (u"salon_and_release", u"Магазин-салон и пункт выдачи товара"),
        )

    point_type = models.CharField(max_length=17, choices=POINT_TYPE, verbose_name="Тип точки", default=u"salon_and_release")

    name = models.CharField(u'Название точки продаж', max_length=255)
    address = models.CharField(u'Адрес', max_length=255)
    latitude = models.FloatField(u'Широта', null=True, blank=True)
    longitude = models.FloatField(u'Долгота', null=True, blank=True)
    organ     = models.ForeignKey(Organization)
    pricelist_name = models.CharField(u'Название прайслиста', max_length=255)
    pricelist_url = models.CharField(u'юрл прайслиста', max_length=255)
    user = models.ForeignKey(User, null=True, blank=True)


    def __unicode__(self):
        return u'%s, %s' % (self.name, self.address)
    
class Offer(models.Model):
    product = models.ForeignKey(Product)
    salepoint = models.ForeignKey(Salepoint)
    price = models.FloatField(u'Цена')
    created = models.DateTimeField()
    
    def __unicode__(self):
        return u'%s в магазине %s' % (self.product, self.salepoint)
    