

from django.contrib import admin
from django.conf.urls import *
from tastypie.api import Api
from models import *
from api import *
from django.conf import settings
v1_api = Api(api_name = 'v1')
v1_api.register(SalepointResource())
v1_api.register(OfferResource())
v1_api.register(ProductResource())
v1_api.register(UserResource())
v1_api.register(WhiteBrandResource())
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'xml_generator.views.home', name='home'),
    # url(r'^xml_generator/', include('xml_generator.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
    url(r'^generate-xml/$', 'xml_generator.views.generate_xml'),
    url(r'^view-data/$', 'xml_generator.views.view_data'),
    url(r'^admin_tools/', include('admin_tools.urls')),
    #(r'^admins/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/eugene/Documents/xml_generator/xml_generator/templates/templates/admin/static', 'show_indexes': True}),
)


