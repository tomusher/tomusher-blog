from django.conf.urls.defaults import patterns, include, url
from base.views import HomeView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from blog.views import PostListView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tomusher.views.home', name='home'),
    # url(r'^tomusher/', include('tomusher.foo.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root' : settings.MEDIA_ROOT,
    }),

    url(r'$^', HomeView.as_view(), name="home"),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),

    url(r'^', include('blog.urls')),
)

urlpatterns += staticfiles_urlpatterns()
