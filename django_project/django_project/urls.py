# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from api.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

	#url(r'^api/(?P<off1>.+)/(?P<off2>.+)/$', api_view),
	url(r'^api/$', api_view),
	url(r'^$', home_view),
    # Examples:
    # url(r'^$', 'lyrics.views.home', name='home'),
    # url(r'^lyrics/', include('lyrics.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
