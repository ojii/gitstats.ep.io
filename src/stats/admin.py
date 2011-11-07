# -*- coding: utf-8 -*-
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.functional import update_wrapper
from stats.models import Repository, Author


class AuthorAdmin(admin.ModelAdmin):
    search_fields = ['author_string']
    actions = ['merge_action']

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.module_name

        urlpatterns = super(AuthorAdmin, self).get_urls()
        return patterns('',
            url(r'^merge/(?P<pk>\d+)/(?P<others>[\d,]+)/$',
                wrap(self.merge_view),
                name='%s_%s_merge' % info),
        ) + urlpatterns
    
    def merge_action(self, request, queryset):
        context = RequestContext(request)
        context['title'] = "Select main author"
        context['queryset'] = queryset
        context['primary_keys'] = queryset.values_list('pk', flat=True)
        return render_to_response('admin/stats/merge.html', context)
    merge_action.short_description = 'Merge users'
    
    def merge_view(self, request, pk, others):
        other_authors = Author.objects.filter(pk__in=others.split(','))
        main = Author.objects.get(pk=pk)
        main.aliases = ','.join(other_authors.values_list('author_string', flat=True))
        main.save()
        other_authors.delete()
        return HttpResponseRedirect(reverse('admin:stats_author_changelist'))


admin.site.register(Author, AuthorAdmin)

admin.site.register(Repository,
    readonly_fields=['slug', 'built', 'updated'],
    list_display=['__unicode__', 'built', 'autobuild', 'updated'],
)
