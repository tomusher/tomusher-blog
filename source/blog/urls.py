from django.conf.urls.defaults import patterns, include, url
from .views import PostDetailView, PostListView
from .feeds import LatestPostsFeed

urlpatterns = patterns('',
    url(r'^(?P<cat>[\w-]+)/$', PostListView.as_view(), name="post_list"),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[\w-]+)/$', PostDetailView.as_view(), name="post_detail"),
    url(r'^feed/$', LatestPostsFeed()),
)

