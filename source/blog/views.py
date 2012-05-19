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
    
    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        category = self.kwargs['cat']
        if category=='all':
            context['category'] = "All"
        else:
            temp_post = Post(category=category)
            context['category'] = temp_post.get_category_display() 
        return context

