#!/usr/bin/python
# -*- coding: utf-8 -*-
from stats.core import Repo
import argparse
import datetime
import time


def render(**context):
    from django import template
    return template.Template("""
    <html>
        <head>
            <meta charset="utf-8">
            <title>Git Statistics</title>
        </head>
        <body>
            <div id="chart1" style="width: 100%; height: 400px">Loading...</div>
            <div id="chart2" style="width: 100%; height: 400px">Loading...</div>
        </body>
        <script src="https://ajax.googleapis.com/ajax/libs/mootools/1.3.0/mootools-yui-compressed.js" type="text/javascript"></script>
        <script src="js/adapters/mootools-adapter.js" type="text/javascript"></script>
        <script src="js/highcharts.js" type="text/javascript"></script>
        {{ charts|safe }}
    </html>
    """).render(template.Context(context))


def main(repopath):
    from django.conf import settings
    settings.configure()
    from highcharts.core import Charts
    
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
        authors = stats.get_active_authors_by_month(year, month)
        month_new_authors = len(authors.difference(total_authors))
        total_authors.update(authors)
        timestamp = time.mktime(datetime.date(year=year, month=month, day=1).timetuple()) * 1000
        total_commits += commitcount
        active_authors.append((timestamp, authorcount))
        commits.append((timestamp, commitcount))
        cumulative_authors.append((timestamp, len(total_authors)))
        cumulative_commits.append((timestamp, total_commits))
        new_authors.append((timestamp, month_new_authors))

    charts = Charts()
    charts.addChart('chart1').chart(
        renderTo='chart1',
        zoomType='x',
    ).title(
        text='django CMS authors statistics'
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
    charts.addChart('chart2').chart(
        renderTo='chart2',
        zoomType='x',
    ).title(
        text='django CMS commit statistics'
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
    
    with open('static/index.html', 'w') as fobj:
        fobj.write(render(charts=charts))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('repopath', help='Path to a git repo')
    args = parser.parse_args()
    main(repopath=args.repopath)
