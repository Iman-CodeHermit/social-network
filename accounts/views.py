import random
from utils import send_otp_code
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm
from django.contrib import messages

# Create your views here.

class UserRegistrationView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'



    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone_number'], code=random_code)
            request.session['user_registration_info'] = {
                'phone_number': form.cleaned_data['phone_number'],
                'email': form.cleaned_data['email'],
                'username': form.cleaned_data['username'],
                'password': form.cleaned_data['password'],
            }
            messages.success(request, 'We sent your code!', 'success')
            return redirect('accounts:verify_code')
        return redirect('home:home')

