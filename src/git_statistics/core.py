# -*- coding: utf-8 -*-
from dulwich import repo
from git_statistics.api import RepoStatistics


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
