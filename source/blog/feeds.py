from django.contrib.syndication.views import Feed
from .models import Post

class LatestPostsFeed(Feed):
    title = "tomusher.com Latest Posts"
    link = "/"
    description = "All the latest posts from tomusher.com"

    def items(self):
        return Post.objects.published()[:10] 

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content_html
