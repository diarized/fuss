from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/fuss/'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fuss/', include('fuss.urls')),
    url(r'^lunch/', include('lunch.urls')),
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/favicon.ico'}),
)


