# -*- coding: utf-8 -*-
from dateutil import rrule
from git_statistics.utils import commit_dt, simple_method_cacher, complex_method_cacher
from collections import defaultdict
import datetime


class UserStatistics(object):
    pass


class RepoStatistics(object):
    def __init__(self, repo):
        self.repo = repo
    
    @simple_method_cacher    
    def get_commits(self):
        return list(self.repo.itercommits())
    
    @simple_method_cacher
    def get_first_commit(self):
        return min(self.get_commits(), key=commit_dt)
    
    @simple_method_cacher
    def get_first_commit_date(self):
        return commit_dt(self.get_first_commit())
        
    @simple_method_cacher
    def get_age(self):
        now = datetime.datetime.now()
        delta = now - self.get_first_commit_date()
        return delta.days
    
    def get_active_days_count(self):
        days = set()
        for commit in self.get_commits():
            days.add(commit_dt(commit.commit_d).strftime('%Y-%m-%d'))
        return len(days)
    
    @simple_method_cacher
    def get_active_day_percentage(self):
        return float(self.get_active_days_count()) / float(self.get_age()) * 100
    
    def get_file_count(self):
        pass
    
    def get_total_lines_of_code(self):
        pass
    
    def get_added_lines_of_code(self):
        pass
    
    def get_removed_lines_of_code(self):
        pass
    
    @simple_method_cacher
    def get_commit_count(self):
        return len(self.get_commits())

    @simple_method_cacher
    def get_average_commits_per_active_day(self):
        return float(self.get_commit_count()) / float(self.get_active_days_count())
    
    @simple_method_cacher
    def get_average_commits_per_day(self):
        return float(self.get_commit_count()) / float(self.get_age())
    
    @simple_method_cacher
    def get_authors(self):
        authors = set()
        for commit in self.get_commits():
            authors.add(commit.author)
        return authors
    
    @simple_method_cacher
    def get_author_count(self):
        return len(self.get_authors())
    
    @simple_method_cacher
    def get_average_commits_per_author(self):
        return float(self.get_commit_count()) / float(self.get_author_count())
    
    @complex_method_cacher
    def get_commits_by_month(self, year, month):
        cache = defaultdict(list)
        default = []
        for commit in self.get_commits():
            cdt = commit_dt(commit)
            args = (cdt.year, cdt.month)
            cache[args].append(commit)
        return cache, default
    
    @simple_method_cacher
    def get_active_authors_by_month(self, year, month):
        authors = set()
        for commit in self.get_commits_by_month(year, month):
            authors.add(commit.author)
        return authors
    
    @simple_method_cacher
    def get_active_author_count_by_month(self, year, month):
        return len(self.get_active_authors_by_month(year, month))
    
    def iter_history_months(self):
        now = datetime.datetime.now()
        start = now - datetime.timedelta(days=self.get_age())
        for dt in rrule.rrule(rrule.MONTHLY, dtstart=start, until=now):
            yield dt.year, dt.month
    
    def iter_active_authors_by_month(self):
        for year, month in self.iter_history_months():
            yield year, month, self.get_active_authors_by_month(year, month)
            
    def iter_active_author_count_by_month(self):
        for year, month, authors in self.iter_active_authors_by_month():
            yield year, month, len(authors)
            
    def iter_commit_count_by_month(self):
        for year, month in self.iter_history_months():
            yield year, month, len(self.get_commits_by_month(year, month))
