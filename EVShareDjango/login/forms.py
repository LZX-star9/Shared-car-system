from django import forms
from system.models import User

from .models import CaptchaModel

class LoginForm(forms.Form):
    username = forms.CharField(min_length=2, max_length=20,label="Username",
                               error_messages={
                                  'min_length': 'Please enter at least 2 characters',
                                  'max_length': 'Please enter less than 20 characters',
                               })
    password = forms.CharField(label="Password",widget=forms.PasswordInput)
    remember = forms.IntegerField(required=False)

class RegisterForm(forms.Form):
    username = forms.CharField(min_length=2, max_length=20,label="Username")
    password = forms.CharField(label="Password",widget=forms.PasswordInput)
    surname = forms.CharField(min_length=2, max_length=20,label="Surname")
    firstname = forms.CharField(min_length=2, max_length=20,label="Firstname")
    email = forms.EmailField(label="Email")
    captcha = forms.CharField(max_length=4,min_length=4,label="Captcha")
    telephone = forms.CharField(min_length=9, max_length=20,label="Telephone")
    confirm_password = forms.CharField(label="Confirm Password",widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError("Email has already been registered")
        return email

    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        email = self.cleaned_data.get('email')
        exists = CaptchaModel.objects.filter(email=email,captcha=captcha).exists()
        if not exists:
            raise forms.ValidationError("Invalid captcha")
        return captcha

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return confirm_password

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['surname', 'firstname', 'telephone', 'email', 'image']
        widgets = {
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
