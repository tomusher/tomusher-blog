from django.conf.urls.defaults import patterns, include, url
from base.views import HomeView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from filebrowser.sites import site
from django.conf import settings
from blog.views import PostDetailView, PostListView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tomusher.views.home', name='home'),
    # url(r'^tomusher/', include('tomusher.foo.urls')),

    url(r'$^', HomeView.as_view(), name="home"),
    url(r'^posts/(?P<slug>[\w-]+)/$', PostDetailView.as_view(), name="post_detail"),
    url(r'^(?P<slug>[\w-]+)/$', PostListView.as_view(), name="post_list"),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root' : settings.MEDIA_ROOT,
    }),

    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^grappelli/', include('grappelli.urls')),
)

urlpatterns += staticfiles_urlpatterns()
