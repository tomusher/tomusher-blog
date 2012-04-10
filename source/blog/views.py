from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.views.generic.list import ListView
from .models import Post

class PostDetailView(DetailView):
    context_object_name = "post"
    queryset = Post.objects.all()

    def get_object(self):
        if self.request.user.is_authenticated():
            return get_object_or_404(Post, slug=self.kwargs['slug'])
        else:
            return get_object_or_404(Post, slug=self.kwargs['slug'], status=1)

class PostListView(ListView):
    context_object_name = "posts"
    template_name = "blog/post_list.html"
    
    def get_queryset(self):
        category = self.kwargs['cat']
        if category=='all':
            posts = Post.objects.published()
        else:
            posts = Post.objects.published().filter(category=category)

        return posts
