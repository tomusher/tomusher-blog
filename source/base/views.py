from django.views.generic.base import TemplateView
from blog.models import Post

class HomeView(TemplateView):
    "Home page"
    template_name = "base/home.html"

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated():
            posts = Post.objects.all().order_by('-pub_date')[:20]
        else:
            posts = Post.objects.published()[:20]
        return {'posts': posts}
