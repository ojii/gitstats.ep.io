# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from stats.models import Repository
import settings

def repodata_patterns():
    if not settings.DEBUG:
        return []
    return patterns('',
        url(r'repodata/(?P<path>.*)$', 'django.views.static.serve', kwargs={'document_root': settings.DATA_DIR}),
    )

urlpatterns = patterns('',
    url(r'^', include(repodata_patterns())),
    url(r'^$',
        ListView.as_view(
            queryset=Repository.objects.filter(built=True),
            template_name='index.html'
        ), 
        name='home'
    ),
    url(r'^(?P<slug>[a-zA-Z0-9_-]+)/$',
        DetailView.as_view(
            queryset=Repository.objects.filter(built=True),
            template_name='detail.html'),
        name='repository'
    ),
)
