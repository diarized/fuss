from django.conf.urls import patterns, url
#from django.views.generic import ListView
#from lunch import models
import controller

urlpatterns = patterns('',
        url(r'^$', controller.index),
        url(r'^meals/$', controller.meal),
        url(r'^vendors/$', controller.vendor),
        url(r'^events/$', controller.event),
        url(r'^orders/$', controller.order),
        url(r'^orders/(?P<order_number>\d+)', controller.order),
        #(r'^vendors/$', ListView.as_view(model=models.Vendor,)),
)

