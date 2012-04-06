from django.conf.urls import *

urlpatterns = patterns('xml_generator.analytics.views',
    url(r'^offers/$', 'offers'),
    url(r'^offers/data/$', 'offers_data'),
)