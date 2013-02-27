from django.conf.urls import patterns, url
from django.views.generic import ListView
from lunch import models
import controller

urlpatterns = patterns('',
        url(r'^$', controller.index),
        url(r'^meal$', controller.meal),
        url(r'^vendor$', controller.vendor),
        url(r'^event$', controller.event),
        url(r'^order$', controller.order),
        url(r'^orders/(?P<order_number>\d+)', controller.order),
        (r'^vendors/$', ListView.as_view(model=models.Vendor,)),
)

