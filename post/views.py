from django.shortcuts import render, redirect
from django.views import View
from post.models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

# Create your views here.
class PostDetailView(View):
    def get(self, request, post_id, post_slug):
        post = Post.objects.get(id = post_id, slug = post_slug)
        return render(request, 'post/detail.html', {'post': post})
        

class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, 'post delete successfully!', 'success')
            return redirect('home:home')
        messages.error(request, 'you cant delete this post!', 'danger')
        return render(request, 'post/detail.html')


class PostUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        pass
