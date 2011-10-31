# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from stats.models import Repository


class Command(BaseCommand):
    args = '<name> <repourl>'
    help = 'Add a repo'

    def handle(self, name, repourl, **options):
        repo = Repository.objects.create(name=name, repourl=repourl)
        repo.build()
        self.stdout.write('Successfully built repo "%s"\n' % repo)
