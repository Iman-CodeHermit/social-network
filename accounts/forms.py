from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'username')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('password dont match!')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user    


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'password', 'last_login')
        password = ReadOnlyPasswordHashField(help_text='You Can Change Password Using<a href=\"../password/\">This Form</a>')


class UserRegistrationForm(forms.Form):
    phone_number = forms.CharField(required=True, max_length= 11, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('this email already exists.')
        return email

    def clean_phone(self):
        phone_number = self.cleaned_data['phone_number']
        user = User.objects.filter(phone_number = phone_number).exists()
        if user:
            raise ValidationError('this phone number already exists.')
        return phone_number


class VerifyCodeForm(forms.ModelForm):
    code = forms.ImageField()
