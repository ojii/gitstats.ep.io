# -*- coding: utf-8 -*-
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import simplejson


class Dumper(object):
    def __init__(self, chart, name):
        self._chart = chart
        self._name = name
        
    def __call__(self, **kwargs):
        self._chart._data[self._name] = kwargs
        return self._chart
    
    def append(self, data):
        if self._name not in self._chart._data:
            self._chart._data[self._name] = []
        self._chart._data[self._name].append(data)
        return self._chart
        


class Chart(object):
    def __init__(self):
        self._data = {}
        
    def __getattr__(self, attr):
        return Dumper(self, attr)


class Charts(object):
    def __init__(self, container):
        self.charts = []
        self.container = container
    
    def __str__(self):
        charts = [chart._data for chart in self.charts]
        data = {
            'container': self.container,
            'charts': charts
        }
        json = simplejson.dumps(data, cls=DjangoJSONEncoder)
        return 'window.addEvent("domready", function(){new PyHighCharts(%s);});' % json
    
    def new_chart(self):
        chart = Chart()
        self.charts.append(chart)
        return chart
