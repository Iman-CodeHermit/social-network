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
    phone_number = forms.CharField(required=True, max_length=11, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),label='Confirm Password')

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('this email already exists.')

        if 'root' or 'admin' in email:
            raise ValidationError('this email cannot contain "root" "admin"')
        return email

    def clean_phone(self):
        phone_number = self.cleaned_data['phone_number']
        user = User.objects.filter(phone_number=phone_number).exists()
        if user:
            raise ValidationError('this phone number already exists.')
        return phone_number

    def clean(self):
        cd = super().clean()
        p1 = cd.get('password')
        p2 = cd.get('confirm_password')

        if p1 and p2 and p1 != p2:
            raise ValidationError('password must match')


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()


class UserLoginForm(forms.Form):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'birthday', 'bio')
        widget = {
            'birthday': forms.DateInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'bio': forms.TextInput(attrs={'class': 'form-control'})
        }
