# -*- coding: utf-8 -*
from django.contrib.gis.db import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth.models import User
from datetime import datetime

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

    class Meta:
        verbose_name = u"белый бренд"
        verbose_name_plural = u'белые бренды'

class Manufacturer(models.Model):
    name = models.CharField(u'Производитель', max_length=255, blank=True, null=True)
    def __unicode__(self):
        return u'%s' % self.name
    class Meta:
        verbose_name = u"Производитель"
        verbose_name_plural = u'Производители'
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

    class Meta:
        verbose_name = u"Страна"
        verbose_name_plural = u'Страны'
    #ext_id = models.IntegerField(verbose_name=u'Ключ Neiron',
    #    help_text=u'PK страны в системе Neiron',
    #    primary_key=True)
    
class ProductManager(models.Manager):
    def get_query_set(self):
        return super(ProductManager, self).get_query_set()\
            .select_related('manufacturer', 'white_brand').filter(is_redundant=False)

class Product(models.Model):
    title = models.CharField(verbose_name=u'Название', max_length=255)
    title_extra = models.CharField(u'Доп. название', max_length=255, blank=True, null=True)
    source_code = models.CharField(max_length=128)
    source_type = models.CharField(max_length=255)
    manufacturer = models.ForeignKey(Manufacturer, verbose_name=u'Производитель',blank=True, null=True)
    country = models.ForeignKey(Country, verbose_name=u'Страна',blank=True, null=True)
    white_brand = models.ForeignKey(WhiteBrand, blank=True, null=True, verbose_name=u"категория")
    is_new = models.BooleanField(u'Новый', help_text='Этот продукт был создан пользователем и еще не прошел модерацию')
    user = models.ForeignKey(User, null=True, blank=True, help_text='Тот, кто добавил этот продукт')
    product_moderated = models.ForeignKey('self',null=True,blank=True, help_text='Ссылается на эталонный проверенный модератором продуктом, если не пусто')
    type = models.CharField(u'тип продукта', max_length=255, blank=True, null=True)
    is_redundant = models.BooleanField(u'не нужный', help_text='Этот продукт не нужен?', default=False)
    sort_weight = models.IntegerField(u'вес сортировки', help_text='Популярному более продукту вес меньший соотвествует', null=True, blank=True, default=100)
    objects = ProductManager()
    class Meta:
        verbose_name = u"продукт"
        verbose_name_plural = u'продукты'

    def __unicode__(self):
        return u'%s. %s (%s)' % (self.title, self.title_extra, self.manufacturer.name)

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
    class Meta:
        verbose_name = u"Организация"
        verbose_name_plural = u'Организации'

    def __unicode__(self):
        return self.name
    
class OfferSalepointManager(models.Manager):
    def get_query_set(self):
        return super(OfferSalepointManager, self).get_query_set()\
            .annotate(offers_count=models.Count('offer'))\
            .select_related('organ')

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

    point_type = models.CharField(max_length=17, choices=POINT_TYPE, verbose_name=u"Тип точки", default=u"salon_and_release")

    variation = models.CharField(max_length=17, choices=VARIATION_TYPE, verbose_name=u"заправка\продукты", default=u"product",null=True, blank=True)
    is_new = models.BooleanField(u'Новая', help_text=u'Эта точка продаж была создана пользователем и еще не прошла модерацию')
    status = models.CharField(max_length=12, choices=STATUS, verbose_name=u"статус", default=u"on")
    name = models.CharField(u'Название', max_length=255)
    address = models.CharField(u'Адрес', max_length=255)
    latitude = models.FloatField(u'Широта', null=True, blank=True)
    longitude = models.FloatField(u'Долгота', null=True, blank=True)
    organ     = models.ForeignKey(Organization, verbose_name="организация", null=True, blank=True)
    #pricelist_name = models.CharField(u'Название прайслиста', max_length=255, default=u"введите название прайслиста")
    #pricelist_url = models.CharField(u'uрл прайслиста', max_length=255, default=u'введите url Прайслиста')
    user = models.ForeignKey(User, null=True, blank=True, verbose_name=u"сборщик предложений")
    city = models.CharField(u'Город', max_length=255, default=u"Челябинск")
    last_modified_time = models.DateTimeField(null=True, blank=True, verbose_name=u"обновлена")
    #salepoint_moderated = models.ForeignKey('self',null=True,blank=True, verbose_name="отмодерированная точка продаж", help_text='Ссылается на эталонную проверенную модератором точку продаж, если не пусто')
    is_redundant = models.BooleanField(u'Не нужная', help_text=u'Этот точка продаж нужна?', default=False)
    
    with_offers = OfferSalepointManager()
    objects = models.Manager()

    class Meta:
        verbose_name = u"точка продаж"
        verbose_name_plural = u'точки продаж'

    def __unicode__(self):
        return u'%s, %s, %s, %s' % (self.organ.name, self.name, self.city, self.address)
    
    def offers_count(self):
        return Offer.objects.filter(salepoint=self, is_redundant=False).count()
    offers_count.short_description = u'предложений'
    
class OfferManager(models.Manager):
    def get_query_set(self):
        return super(OfferManager, self).get_query_set()\
            .select_related('salepoint', 'product').filter(is_redundant=False).order_by('-created')
            
class Offer(models.Model):
    product = models.ForeignKey(Product, verbose_name=u"Продукт")
    salepoint = models.ForeignKey(Salepoint, verbose_name=u"Точка продаж")
    price = models.FloatField(u'Цена')
    created = models.DateTimeField(verbose_name=u"время создания")
    is_redundant = models.BooleanField(u'Не нужно', help_text=u'Это предложение нужно?', default=False)
    objects = OfferManager()
    all_objects = models.GeoManager()

    class Meta:
        verbose_name = u"предложение"
        verbose_name_plural = u'предложения'

    def __unicode__(self):
        return u'%s в магазине %s' % (self.product, self.salepoint)
    
    def save(self, *args, **kwargs):
        self.created = datetime.now()
        super(Offer, self).save(*args, **kwargs)






class TaskManager(models.Manager):
    def get_query_set(self):
        return super(TaskManager, self).get_query_set()\
            .select_related('user')
            
class Task(models.Model):
    user   = models.ForeignKey(User, null=True, blank=False, verbose_name=u"сборщик предложений")
    salepoint = models.ManyToManyField(Salepoint, null=True, blank=False, verbose_name=u"Точки продаж")
    period = models.IntegerField(null=True, blank=True, verbose_name=u'периодичность')
    #date_start_for_period = models.DateTimeField(null=True, blank=True, verbose_name=u"время создания для периодличности")
    date_to_execute = models.DateTimeField(null=True, blank=False, verbose_name=u"дата выполнения")
    accomplished = models.BooleanField(u'выполнено ли', default=False)
    comment = models.TextField(null=True, blank=True, verbose_name=u'комментарии сборщика по заданию, причина не выполения')
    is_pattern = models.BooleanField(default=False, verbose_name=u'шаблонное задание')
    objects = TaskManager()

    class Meta:
        verbose_name = u"задание"
        verbose_name_plural = u'задания'
        #ordering = ['salepoint__organ__name',]
    def __unicode__(self):
        return u'задание номер %s для %s' % (self.pk, self.user.username)


class Simple_Logs(models.Model):
    TARGET_TYPE = (
        (u"phone", u"сборщик"),
        (u"server", u"сервер"),
        )
    LOG_LEVEL = (
        (u"debug", u"дебаг"),
        (u"info", u"инфо"),
        )
    user = models.ForeignKey(User, verbose_name=u"сборщик предложений")
    origin = models.CharField(max_length=17, choices=TARGET_TYPE, verbose_name=u"источник", default=u"server")
    target = models.CharField(max_length=17, choices=TARGET_TYPE, verbose_name=u"кто цель", default=u"phone")
    log_level = models.CharField(max_length=17, choices=LOG_LEVEL, verbose_name=u"уровень лога", default=u"info")
    message = models.TextField(verbose_name=u'текст сообщения')
    created = models.DateTimeField(verbose_name=u"дата лога", default=datetime.now)

    class Meta:
        verbose_name = u"лог"
        verbose_name_plural = u'логи'
        #ordering = ['salepoint__organ__name',]
    def __unicode__(self):
        return u'лог  %s' % (self.pk)