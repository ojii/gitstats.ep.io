# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from stats.builder import build
from stats.utils import auto_slug, update_git
import os


class AliasManager(models.Manager):
    def __init__(self):
        self._cache = None
        super(AliasManager, self).__init__()
        
    @property
    def cache(self):
        if self._cache is None:
            self.fill_cache()
        return self._cache

    def fill_cache(self):
        self._cache = {}
        for author in self.all():
            self._cache[author.author_string] = author
            for alias in author.aliases.split(','):
                self._cache[alias] = author
    
    def get_or_create(self, author_string):
        if author_string in self.cache:
            return self.cache[author_string]
        try:
            author = self.get(author_string=author_string)
        except self.model.DoesNotExist:
            name, raw_email = author_string.rsplit(' ', 1)
            email = raw_email[1:-1]
            author = super(AliasManager, self).create(name=name, email=email, author_string=author_string)
        self.cache[author_string] = author
        return author


class Author(models.Model):
    author_string = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    aliases = models.TextField(default='')
    
    objects = AliasManager()
    
    def __unicode__(self):
        return self.author_string


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
    
    @property
    def repodatapath(self):
        return os.path.join(settings.DATA_DIR, '%s.js' % self.slug)
    
    def build(self):
        repodir = os.path.join(settings.REPO_DIR, self.slug)
        update_git(self.repourl, repodir)
        data = build(repodir, self.name)
        jspath = self.repodatapath
        with open(jspath, 'w') as fobj:
            fobj.write(str(data))
        self.built = True
        self.save()
    
auto_slug(Repository, 'slug', 'name')
