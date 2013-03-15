from django.conf.urls import patterns, url
from django.views.generic import ListView
from lunch import models
import controller

urlpatterns = patterns('',
        url(r'^$', controller.index),
#        url(r'^vendors/$', ListView.as_view(model=models.Vendor,)),
        url(r'^vendors/$', controller.vendor),
        url(r'^meals/(?P<vendor_id>\d+)$', controller.meal),
        url(r'^orders/(?P<event_id>\d+)$', controller.order),
        url(r'^event$', controller.event),
)

