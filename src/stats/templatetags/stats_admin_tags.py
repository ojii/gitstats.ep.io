# -*- coding: utf-8 -*-
from django import template


register = template.Library()

@register.filter
def get_others(main, primary_keys):
    return ','.join([str(pk) for pk in primary_keys if pk != main.pk])
