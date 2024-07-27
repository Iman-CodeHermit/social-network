from django.shortcuts import render
from django.views import View
from post.models import Post
# Create your views here.
class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'home/home.html', {'posts': posts})