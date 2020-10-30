from django import forms
from django.contrib.auth.models import User
import re

def password_check(password):
    pattern = re.compile(r"")

def email_check(email):
    pattern = re.compile(r"\"?([-a-zA-Z0-9.'?{}]+@\w+\.\w+)\"?")
    return re.match(pattern,email)

class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    #验证规则
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise forms.ValidationError('your username must be least 3 charcters long')
        elif len(username) > 20:
            raise forms.ValidationError('your username must be less than 20 charcters ')
        else:
            filter_result = User.objects.filter(username=username)
            if filter_result:
                raise forms.ValidationError('your username already exsits')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email_check(email):
            filter_result = User.objects.filter(email=email)
            if len(filter_result) > 0:
                raise forms.ValidationError("your email already exists")
        else:
            raise forms.ValidationError("Please enter a valid email")

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 3:
            raise forms.ValidationError("your password is too short")
        elif len(password1) > 20:
            raise forms.ValidationError("your password is too long")

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Password mismatch Please enter again')

        return password2


class LoginForm(forms.Form):
    username = forms.CharField(label='Username or Email', max_length=50)
    password = forms.CharField(label='Password', max_length=20,widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        #邮箱登录
        if email_check(username):
            result = User.objects.filter(email__exact=username)
            if  not result:
                raise forms.ValidationError('your email does not exist ')
        else:
            result = User.objects.filter(username__exact=username)
            if not result:
                raise forms.ValidationError('This username does not exist')
        return username

    # def clean_password(self):
    #     result = User.objects.filter()


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='Old Password', max_length=50,widget=forms.PasswordInput)
    password1 = forms.CharField(label='New Password', max_length=50, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', max_length=50, widget=forms.PasswordInput)

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        # if password1 and (6 <= len(password1) <= 20):
        #     return password1
        # else:
        #     forms.ValidationError('password leng 6-20')
        if len(password1) < 6:
            raise forms.ValidationError("your password is too short")
        elif len(password1) > 20:
            raise forms.ValidationError("your password is too long")

        return password1

    def clean_password2(self):
        # password1 = self.cleaned_data.get('password1')
        # password2 = self.cleaned_data.get('password2')
        # if password1 == password2:
        #     if password2:
        #         return password2
        #     else:
        #         forms.ValidationError('Password must be a string or bytes')
        # else:
        #     forms.ValidationError('wrong password')

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 :
            if password1 != password2:
                raise forms.ValidationError("Password mismatch Please enter again")

        return password2




