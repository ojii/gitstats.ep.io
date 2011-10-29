# -*- coding: utf-8 -*-
from django.contrib import admin
from stats.models import Repository

admin.site.register(Repository, readonly_fields=['slug', 'built'])
