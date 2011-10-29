# -*- coding: utf-8 -*-
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import datetime_safe, simplejson
import datetime

class DateJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            d = datetime_safe.new_datetime(o)
            return d.isoformat()
        elif isinstance(o, datetime.date):
            d = datetime_safe.new_date(o)
            return d.isoformat()
        else:
            return super(DateJSONEncoder, self).default(o)


class Dumper(object):
    def __init__(self, chart, name):
        self._chart = chart
        self._name = name
        
    def __call__(self, **kwargs):
        self._chart.data[self._name] = kwargs
        return self._chart
    
    def append(self, data):
        if self._name not in self._chart.data:
            self._chart.data[self._name] = []
        self._chart.data[self._name].append(data)
        return self._chart
        


class Chart(object):
    def __init__(self, name):
        self.name = name
        self.data = {}
        
    def __str__(self):
        json = simplejson.dumps(self.data, cls=DateJSONEncoder)
        return 'window.%s = new Highcharts.Chart(%s);' % (self.name, json)
    
    def __getattr__(self, attr):
        return Dumper(self, attr)


class Charts(object):
    def __init__(self):
        self.charts = []
    
    def __str__(self):
        charts = '\n'.join([str(chart) for chart in self.charts])
        return 'window.addEvent("domready", function(){%s});' % charts
    
    def addChart(self, name):
        chart = Chart(name)
        self.charts.append(chart)
        return chart
