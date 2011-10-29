# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from stats.models import Repository


class Command(BaseCommand):
    args = '<project-slug project-slug ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        if args:
            repos = Repository.objects.filter(slug__in=args)
            if len(repos) != len(args):
                raise CommandError('One or more slug invalid')
        else:
            repos = Repository.objects.all()
        for repo in repos:
            repo.build()
            self.stdout.write('Successfully built repo "%s"\n' % repo)
