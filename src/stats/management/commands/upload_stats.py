# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from stats.models import Repository
import subprocess


class Command(BaseCommand):
    args = '<project-slug>'
    help = 'Uploads stats'

    def handle(self, slug, **options):
        repo = Repository.objects.get(slug=slug)
        subprocess.check_call(['scp', repo.repodatapath, 'vcs@ssh.ep.io:gitstats/repodata/%s.js' % repo.slug])
        subprocess.check_call(['epio', 'django', 'load_stats', repo.slug, '../data/repodata/%s.js' % repo.slug])
