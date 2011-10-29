# -*- coding: utf-8 -*-
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
import os
import subprocess

class Slugifier(object):
    def __init__(self, model, target, source):
        self.model = model
        self.target = target
        self.source = source
        field = self.model._meta.get_field_by_name(self.target)[0]
        self.max_length = field.max_length
        
    def __call__(self, instance, **kwargs):
        if getattr(instance, self.target):
            return
        slug = slugify(getattr(instance, self.source))[:self.max_length]
        current = slug
        index = 0
        while self.model.objects.filter(**{self.target: current}).exists():
            suffix = '-%s' % index
            current = '%s%s'  % (slug[:-len(suffix)], suffix)
            index += 1
        setattr(instance, self.target, current)
    

def auto_slug(model, target, source):
    """
    class MyModel(models.Model):
        name = models.CharField(max_length=255)
        slug = models.SlugField(max_length=255, null=True)
        
    auto_slug(MyModel, 'slug', 'name')
    """
    pre_save.connect(Slugifier(model, target, source), sender=model, weak=False)


def update_git(repourl, repodir):
    # TODO: do this with dulwich, not subprocess
    if os.path.exists(repodir):
        subprocess.check_call(['git', 'fetch', 'origin'], cwd=repodir)
    else:
        subprocess.check_call(['git', 'clone', repourl, repodir])
