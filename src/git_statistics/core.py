# -*- coding: utf-8 -*-
from dulwich import repo
from dulwich.objects import Commit
from git_statistics.api import RepoStatistics
from git_statistics.utils import author_factory
from stats.models import Author


def get_author(obj):
    obj._ensure_parsed()
    return author_factory(getattr(obj, "_author"))

def set_author(obj, author):
    if isinstance(author, Author):
        author = u'%s <%s>' % (author.name, author.email)
    obj._ensure_parsed()
    setattr(obj, "_author", author)
    obj._needs_serialization = True

Commit.author = property(get_author, set_author, doc=Commit.author.__doc__)

class Repo(repo.Repo):
    def itercommits(self):
        walker = self.get_graph_walker()
        while True:
            sha = walker.next()
            if not sha:
                return
            yield self[sha]

    def get_stats(self):
        return RepoStatistics(self)
