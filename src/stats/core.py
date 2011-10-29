# -*- coding: utf-8 -*-
from dulwich import repo
from stats.api import RepoStatistics

def _iter_commits(repo):
    walker = repo.get_graph_walker()
    while True:
        sha = walker.next()
        if not sha:
            return
        yield repo.commit(sha)

def get_author_count(repo_dir):
    repo = Repo(repo_dir)
    s = set()
    for commit in _iter_commits(repo):
        s.add(commit.author)
    return len(s)


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
