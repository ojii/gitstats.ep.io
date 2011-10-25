#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from stats.core import Repo


class Data(object):
    def __init__(self, varname):
        self.varname = varname
        self.lines = []
        
    def _write(self, method, *args):
        formatted_args = ', '.join([json.dumps(arg) for arg in args])
        self.lines.append('%s.%s(%s);' % (self.varname, method, formatted_args))
        
    def __getattr__(self, attr):
        def deco(*args):
            self._write(attr, *args)
        return deco
    
    def __str__(self):
        return '\n'.join(self.lines)


page_template = """
<html>
    <script src="https://www.google.com/jsapi" type="text/javascript"></script>
    <script>
        google.load("visualization", "1", {packages:["corechart"]});
        google.setOnLoadCallback(drawChart);
        function drawChart() {
            var data = new google.visualization.DataTable();
            %(data)s
            var chart = new google.visualization.LineChart(document.getElementById('chart'));
            chart.draw(data, {width: 800, height: 600, title: 'django CMS contributors over time'});
        }
    </script>
    <body>
        <div id="chart"></div>
    </body>
</html>
"""

def main():
    repo = Repo('/home/jonas/workspace/django-cms')
    stats = repo.get_stats()
    
    data = Data('data')
    data.addColumn('string', 'Year - Month')
    data.addColumn('number', 'Active Contributors')
    data.addColumn('number', 'Commits')
    data.addRows(len(list(stats.iter_history_months())))
    
    for index, value in enumerate(stats.iter_active_author_count_by_month()):
        year, month, authorcount = value
        data.setValue(index, 0, '%s - %s' % (year, month))
        data.setValue(index, 1, authorcount)
        commits = len(stats.get_commits_by_month(year, month))
        data.setValue(index, 2, commits)
    
    context = {
        'data': data,
    }
    with open('static/index.html', 'w') as fobj:
        fobj.write(page_template % context)


if __name__ == '__main__':
    main()
