

from django.contrib import admin
from django.conf.urls import *
from tastypie.api import Api
from models import *
from api import *

v1_api = Api(api_name = 'v1')
v1_api.register(SalepointResource())
v1_api.register(OfferResource())
v1_api.register(ProductResource())
v1_api.register(UserResource())

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'xml_generator.views.home', name='home'),
    # url(r'^xml_generator/', include('xml_generator.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
    url(r'^generate-xml/$', 'xml_generator.views.generate_xml')
)
