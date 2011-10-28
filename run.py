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
        <script src="https://ajax.googleapis.com/ajax/libs/mootools/1.3.0/mootools-yui-compressed.js" type="text/javascript"></script>
        <script src="js/adapters/mootools-adapter.js" type="text/javascript"></script>
        <script src="js/highcharts.js" type="text/javascript"></script>
        {{ charts|safe }}
        <body>
            <div id="chart1" style="width: 100%; height: 400px"></div>
            <div id="chart2" style="width: 100%; height: 400px"></div>
        </body>
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
    cumulative_authors = []
    total_authors = set()
    
    for year, month in stats.iter_history_months():
        authorcount = stats.get_active_author_count_by_month(year, month)
        commitcount = len(stats.get_commits_by_month(year, month))
        authors = stats.get_active_authors_by_month(year, month)
        total_authors.update(authors)
        timestamp = time.mktime(datetime.date(year=year, month=month, day=1).timetuple()) * 1000
        active_authors.append((timestamp, authorcount))
        commits.append((timestamp, commitcount))
        cumulative_authors.append((timestamp, len(total_authors)))

    charts = Charts()
    charts.addChart('chart1').chart(
        renderTo='chart1',
        zoomType='x',
    ).title(
        text='django CMS git stats'
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
            'text': 'Commits',
        },
        'opposite': True
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
        'name': 'Commits',
        'data': commits,
        'type': 'line',
        'yAxis': 2,
        'xAxis': 0,
    })
    
    with open('static/index.html', 'w') as fobj:
        fobj.write(render(charts=charts))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('repopath', help='Path to a git repo')
    args = parser.parse_args()
    main(repopath=args.repopath)
