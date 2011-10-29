# -*- coding: utf-8 -*-
import datetime

def simple_method_cacher(method):
    method.cache = {}
    def _decorator(self, *args):
        try:
            value = method.cache[args]
        except KeyError:
            value = method(self, *args)
            method.cache[args] = value
        return value
    _decorator.__name__ = 'simple_method_cacher(%s)' % method.__name__
    return _decorator

def complex_method_cacher(method):
    method.cache = None
    method.default = None
    def _decorator(self, *args):
        if method.cache is None:
            method.cache, method.default = method(self, *args)
        return method.cache.get(args, method.default)
    _decorator.__name__ = 'complex_method_cacher(%s)' % method.__name__
    return _decorator

def commit_dt(commit):
    return datetime.datetime.fromtimestamp(commit.commit_time)
