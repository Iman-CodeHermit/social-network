from django.shortcuts import render
from django.views import View
from post.models import Post

# Create your views here.
class PostDetailView(View):
    def get(self, request, post_id, post_slug):
        post = Post.objects.get(id = post_id, slug = post_slug)
        return render(request, 'post/detail.html', {'post': post})
        