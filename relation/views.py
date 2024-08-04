from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User
from django.views import View
from .models import Relation
from django.contrib import messages

# Create your views here.

class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            messages.error(request, 'you are already following this user!', 'danger')
        else:
            Relation.objects.create(from_user=request.user, to_user=user)
            messages.success(request, 'you followed this user.', 'success')
        return redirect('accounts:user_profile', user_id)


class UserUnfollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request, 'you unfollowed this user!', 'success')
        else:
            messages.error(request, 'you are not followed this user!', 'danger')
        return redirect('accounts:user_profile', user_id)