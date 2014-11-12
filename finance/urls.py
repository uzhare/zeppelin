from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
    url(r'^(?P<ticker>[\w]+)$', view=DisplayView.as_view(),
        name="display"),
    url(r'', view=TickerListView.as_view(),
        name="ticker_list"),
)