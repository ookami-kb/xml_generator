from django.contrib import admin
from django.conf.urls import *
from tastypie.api import Api
from models import *
from api import *
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

v1_api = Api(api_name = 'v1')
v1_api.register(SalepointResource())
v1_api.register(OfferResource())
v1_api.register(ProductResource())
v1_api.register(UserResource())

v1_api.register(WhiteBrandResource())
v1_api.register(FuelResource())
v1_api.register(FuelProductResource())
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'xml_generator.views.home', name='home'),
    # url(r'^xml_generator/', include('xml_generator.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/salepoint/stat/$', 'xml_generator.analytics.admin_views.salepoints_stat'),
    (r'^admin/user/stat/$', 'xml_generator.analytics.admin_views.users_stat'),
    (r'^admin/product-analyt/(?P<product_pk>\d+)/$', 'xml_generator.analytics.views.product_anal'),
    (r'^admin/product-analyt/(?P<product_pk>\d+)/list_salepoint/$', 'xml_generator.analytics.views.product_list_salepoint'),
    (r'^admin/product-analyt/(?P<product_pk>\d+)/(?P<salepoint_pk>\d+)/$', 'xml_generator.analytics.views.product_chart'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
    url(r'^generate-xml/$', 'xml_generator.views.generate_xml'),
    url(r'^view-data/$', 'xml_generator.views.view_data'),
    
    url(r'^analytics/', include('xml_generator.analytics.urls')),
    url(r'^admin_tools/', include('admin_tools.urls')),
)

# serve static content
urlpatterns += staticfiles_urlpatterns()
