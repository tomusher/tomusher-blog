from django.views.generic import DetailView
from .models import Post

class PostDetailView(DetailView):
    context_object_name = "post"
    queryset = Post.objects.all()

    def get_object(self):
        obj = super(PostDetailView, self).get_object()
        return obj
