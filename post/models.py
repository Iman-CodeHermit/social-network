from django.db import models
from accounts.models import User
# Create your models here.

class Post(models.Model):
    body = models.TextField(max_length=250)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.slug}'
