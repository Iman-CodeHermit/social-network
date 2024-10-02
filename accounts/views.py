import random
from utils import send_otp_code
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserRegistrationForm, VerifyCodeForm, UserLoginForm, EditUserForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import OtpCode, User
from post.models import Post
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from relation.models import Relation


# Create your views here.


class UserRegistrationView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)


    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone_number'], code=random_code)
            print(random_code)
            request.session['user_registration_info'] = {
                'phone_number': form.cleaned_data['phone_number'],
                'email': form.cleaned_data['email'],
                'username': form.cleaned_data['username'],
                'password': form.cleaned_data['password'],
            }
            messages.success(request, 'We sent your code!', 'success')
            return redirect('accounts:verify_code')
        return redirect('home:home')


class UserRegisterVerifyView(View):
    form_class = VerifyCodeForm
    template_name = 'accounts/verify_Code.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    
    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                user = User.objects.create_user(
                    phone_number=user_session['phone_number'],
                    email=user_session['email'],
                    username=user_session['username'],
                    password=user_session['password'],
                )
                code_instance.delete()
                login(request, user)
                messages.success(request, 'You Registered', 'success')
                return redirect('home:home')
            else:
                messages.error(request, 'Code is Wrong', 'danger')
                return redirect('accounts:verify_code')
        return redirect('home:home')


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next', None)
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone_number=cd['phone_number'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you logged in Successfully', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.error(request, 'your password or username is wrong', 'warning')
            return render(request, self.template_name, {'form': form})
                

class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You Logged Out Successfully', 'success')
        return redirect('home:home')


class UserProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'


    def get(self, request, user_id):
        is_following = False
        user = get_object_or_404(User, id=user_id)
        posts = Post.objects.filter(user=user)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            is_following = True
        return render(request, self.template_name, {'user': user, 'posts': posts, 'is_following': is_following})


class EditUserView(LoginRequiredMixin, View):
    form_class = EditUserForm
    
    def get(self, request):
        form = self.form_class(instance=request.user)
        return render(request, 'accounts/edit_profile.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'your profile updated successfully', 'success')
        return redirect('accounts:user_profile', request.user.id)
        

class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


class DeleteUserView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user.delete()
        return redirect('home:home')
