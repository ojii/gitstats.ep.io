# -*- coding: utf-8 -*-
from collections import defaultdict
from highcharts.core import Charts
import datetime
import time

def build(repopath, name):
    """
    Returns an instance of `highcharts.core.Charts` filled with the data of
    `repopath`
    """
    from git_statistics.core import Repo
    repo = Repo(repopath)
    stats = repo.get_stats()
    active_authors = []
    commits = []
    total_authors = set()
    cumulative_authors = []
    new_authors = []
    total_commits = 0
    cumulative_commits = []
    
    for year, month in stats.iter_history_months():
        authors = stats.get_active_authors_by_month(year, month)
        authorcount = len(authors)
        commitcount = len(stats.get_commits_by_month(year, month))
        month_new_authors = len(authors.difference(total_authors))
        total_authors.update(authors)
        timestamp = time.mktime(datetime.date(year=year, month=month, day=2).timetuple()) * 1000
        total_commits += commitcount
        active_authors.append((timestamp, authorcount))
        commits.append((timestamp, commitcount))
        cumulative_authors.append((timestamp, len(total_authors)))
        cumulative_commits.append((timestamp, total_commits))
        new_authors.append((timestamp, month_new_authors))
    
    charts = Charts('container')
    charts.new_chart().chart(
        zoomType='x',
    ).title(
        text='%s authors statistics' % name
    ).yAxis.append({
        'title': {
            'text': 'Active authors',
        }
    }).yAxis.append({
        'title': {
            'text': 'Cumulative authors',
        }
    }).yAxis.append({
        'title': {
            'text': 'New authors',
        },
        'opposite': True,
    }).xAxis.append({
        'type': 'datetime',
    }).series.append({
        'name': 'Active authors',
        'data': active_authors,
        'type': 'line',
        'yAxis': 0,
    }).series.append({
        'name': 'Cumulative authors',
        'data': cumulative_authors,
        'type': 'line',
        'yAxis': 1,
        'xAxis': 0,
    }).series.append({
        'name': 'New authors',
        'data': new_authors,
        'type': 'column',
        'yAxis': 2,
        'xAxis': 0,
    })
    charts.new_chart().chart(
        zoomType='x',
    ).title(
        text='%s commit statistics' % name
    ).yAxis.append({
        'title': {
            'text': 'Commits by month',
        },
    }).yAxis.append({
        'title': {
            'text': 'Cumulative commits',
        },
    }).xAxis.append({
        'type': 'datetime',
    }).series.append({
        'name': 'Commits by month',
        'data': commits,
        'type': 'line',
        'yAxis': 0,
        'xAxis': 0,
    }).series.append({
        'name': 'Cumulative commits',
        'data': cumulative_commits,
        'type': 'line',
        'yAxis': 1,
        'xAxis': 0,
    })
    
    return charts
