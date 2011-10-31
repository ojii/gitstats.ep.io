# -*- coding: utf-8 -*-
import datetime



def simple_method_cacher(method):
    def _decorator(self, *args):
        if not hasattr(self, '_%s_cache' % method.__name__):
            setattr(self, '_%s_cache' % method.__name__, {})
        cache = getattr(self, '_%s_cache' % method.__name__)
        try:
            value = cache[args]
        except KeyError:
            value = method(self, *args)
            cache[args] = value
        return value
    _decorator.__name__ = 'simple_method_cacher(%s)' % method.__name__
    return _decorator

def complex_method_cacher(method):
    def _decorator(self, *args):
        if not hasattr(self, '_%s_cache' % method.__name__):
            cache, default = method(self, *args)
            setattr(self, '_%s_cache' % method.__name__, cache)
            setattr(self, '_%s_cache_default' % method.__name__, default)
        else:
            cache = getattr(self, '_%s_cache' % method.__name__)
            default = getattr(self, '_%s_cache_default' % method.__name__)
        return cache.get(args, default)
    _decorator.__name__ = 'complex_method_cacher(%s)' % method.__name__
    return _decorator

def commit_dt(commit):
    return datetime.datetime.fromtimestamp(commit.commit_time)
