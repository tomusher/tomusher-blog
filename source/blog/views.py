from django.views.generic import DetailView
from django.views.generic.list import ListView
from .models import Post

class PostDetailView(DetailView):
    context_object_name = "post"
    queryset = Post.objects.all()

    def get_object(self):
        obj = super(PostDetailView, self).get_object()
        return obj

class PostListView(ListView):
    context_object_name = "posts"
    template_name = "blog/post_list.html"
    
    def get_queryset(self):
        posts = Post.objects.filter(category=self.kwargs['slug']).order_by('-published_date')[:10]
        return posts
