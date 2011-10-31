# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from stats.models import Repository
import shutil


class Command(BaseCommand):
    args = '<project-slug filename>'
    help = 'Closes the specified poll for voting'

    def handle(self, slug, fpath, **options):
        repo = Repository.objects.get(slug=slug)
        if repo.repodatapath != fpath:
            shutil.move(fpath, repo.repodatapath)
        repo.built = True
        repo.save()
