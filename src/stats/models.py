# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from stats.builder import build
from stats.utils import auto_slug, update_git
import os


class Repository(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    repourl = models.CharField(max_length=255, unique=True)
    updated = models.DateTimeField(auto_now=True)
    built = models.BooleanField(default=False)
    autobuild = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Repositories'
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('repository', kwargs={'slug': self.slug})
    
    def build(self):
        repodir = os.path.join(settings.REPO_DIR, self.slug)
        update_git(self.repourl, repodir)
        data = build(repodir, self.name)
        jspath = os.path.join(settings.DATA_DIR, '%s.js' % self.slug)
        with open(jspath, 'w') as fobj:
            fobj.write(str(data))
        self.built = True
        self.save()
    
auto_slug(Repository, 'slug', 'name')
