# -*- coding: utf-8 -*
from django.db import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth.models import User


class WhiteBrand(models.Model):
    name = models.CharField(verbose_name=u'Название', max_length=30)
    ext_id = models.IntegerField(verbose_name=u'Ключ Neiron',
                                 help_text=u'PK бренда в системе Neiron',
                                 primary_key=True)
    factor_specific_key = models.CharField(max_length=1024, null=True, blank=True)
    factor_specific_unit = models.CharField(max_length=30, null=True, blank=True)
    factor_specific_value = models.FloatField(null=True, blank=True)
    def __unicode__(self):
        return self.name

class Manufacturer(models.Model):
    name = models.CharField(u'Производитель', max_length=255, blank=True, null=True)
    def __unicode__(self):
        return u'%s' % self.name

    '''
    def save(self, *args, **kwargs):
        try:
            self.pk = Manufacturer.objects.get(name=self.name).pk
        except:
            self.pk = None
            #pr =  self.logic()
        return super(Manufacturer, self).save(*args, **kwargs)
    '''
    #ext_id = models.IntegerField(verbose_name=u'Ключ Neiron',
    #    help_text=u'PK производителя в системе Neiron',
    #    primary_key=True)

class Country(models.Model):
    name = models.CharField(u'Страна', max_length=255, blank=True, null=True)
    '''
    def save(self, *args, **kwargs):
        try:
            self.pk = Country.objects.get(name=self.name).pk
        except:
            self.pk = None
        #pr =  self.logic()
        return super(Country, self).save(*args, **kwargs)
    '''
    def __unicode__(self):
        return u'%s' % self.name

    #ext_id = models.IntegerField(verbose_name=u'Ключ Neiron',
    #    help_text=u'PK страны в системе Neiron',
    #    primary_key=True)
    
class Product(models.Model):
    title = models.CharField(verbose_name=u'Название', max_length=255)
    title_extra = models.CharField(u'Доп. название', max_length=255, blank=True, null=True)
    source_code = models.IntegerField()
    source_type = models.CharField(max_length=255)
    manufacturer = models.ForeignKey(Manufacturer, verbose_name=u'Производитель',blank=True, null=True)
    country = models.ForeignKey(Country, verbose_name=u'Страна',blank=True, null=True)
    white_brand = models.ForeignKey(WhiteBrand, blank=True, null=True, verbose_name="Белый бренд: лишь для съестных продуктов")
    is_new = models.BooleanField(u'Новый', help_text='Этот продукт был создан пользователем и еще не прошел модерацию')
    user = models.ForeignKey(User, null=True, blank=True, help_text='Тот, кто добавил этот продукт')
    product_moderated = models.ForeignKey('self',null=True,blank=True, help_text='Ссылается на эталонный проверенный модератором продуктом, если не пусто')
    type = models.CharField(u'тип продукта', max_length=255, blank=True, null=True)
    is_redundant = models.BooleanField(u'не нужный', help_text='Этот продукт не нужен?', default=False)

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
    #ext_id = models.IntegerField(verbose_name=u'Ключ Neiron',
    #    help_text=u'PK организации в системе Neiron',
    #    primary_key=True)

    def __unicode__(self):
        return self.name


class Salepoint(models.Model):
    POINT_TYPE = (
        (u"salon", u"Магазин-салон"),
        (u"release", u"Пункт выдачи товара"),
        (u"salon_and_release", u"Магазин-салон и пункт выдачи товара"),
        )

    VARIATION_TYPE = (
        (u"fuel", u"заправка"),
        (u"product", u"продуктовая"),
        (u'medecine', u"медецина"),
        )

    STATUS = (
        (u"off", u"Выключен"),
        (u"verification", u"На проверке"),
        (u"activation", u"Включается"),
        (u"on", u"Включен"),
        )

    point_type = models.CharField(max_length=17, choices=POINT_TYPE, verbose_name="Тип точки", default=u"salon_and_release")

    variation = models.CharField(max_length=17, choices=VARIATION_TYPE, verbose_name="заправка\продукты", default=u"product",null=True, blank=True)
    is_new = models.BooleanField(u'Новая', help_text='Эта точка продаж была создана пользователем и еще не прошла модерацию')
    status = models.CharField(max_length=12, choices=STATUS, verbose_name="статус")
    name = models.CharField(u'Название точки продаж', max_length=255)
    address = models.CharField(u'Адрес', max_length=255)
    latitude = models.FloatField(u'Широта', null=True, blank=True)
    longitude = models.FloatField(u'Долгота', null=True, blank=True)
    organ     = models.ForeignKey(Organization, verbose_name="организация")
    pricelist_name = models.CharField(u'Название прайслиста', max_length=255)
    pricelist_url = models.CharField(u'юрл прайслиста', max_length=255)
    user = models.ForeignKey(User, null=True, blank=True, verbose_name="сборщик предложений")
    city = models.CharField(u'Город', max_length=255)
    last_modified_time = models.DateTimeField(null=True, blank=True, verbose_name="время обновления")
    salepoint_moderated = models.ForeignKey('self',null=True,blank=True, verbose_name="отмодерированная точка продаж", help_text='Ссылается на эталонную проверенную модератором точку продаж, если не пусто')
    is_redundant = models.BooleanField(u'Не нужная', help_text='Эта точка продаж нужна?', default=False)
    def __unicode__(self):
        return u'%s, %s' % (self.name, self.address)
    
class Offer(models.Model):
    product = models.ForeignKey(Product, verbose_name="Продукт")
    salepoint = models.ForeignKey(Salepoint, verbose_name="Точка продаж")
    price = models.FloatField(u'Цена')
    created = models.DateTimeField(verbose_name="время создания")


    
    def __unicode__(self):
        return u'%s в магазине %s' % (self.product, self.salepoint)
    