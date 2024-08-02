from django.db import models
from accounts.models import User
# Create your models here.

class Post(models.Model):
    body = models.TextField(max_length=250)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.slug}'

    def Likes_count(self):
        return self.pvote.count()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pcomment')
    body = models.TextField(max_length=250)
    is_reply = models.BooleanField(default=False)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='rcomment', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.user}-{self.body[:30]}'


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uvote')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pvote')

    def __str__(self):
        return f'{self.user} liked {self.post.slug}'

