from django.shortcuts import redirect, reverse, get_object_or_404
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from .form import RegisterForm, LoginForm, ChangePasswordForm
from django.contrib.auth.decorators import login_required
import json
def register_view(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request,'register.html', {'form': form})
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']
            # print(passwd1,passwd2)
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return HttpResponseRedirect('/myuser/login/')
        else:
            error_msg = form.errors.as_json()
            error_msg = json.dumps(error_msg)
            return render(request,'register.html',locals())
        #     if passwd1 == passwd2:
        #         if not User.objects.filter(username=user):
        #             d = dict(username=user, password=passwd1, is_staff=1, is_superuser=1,email=email)
        #             user = User.objects.create_user(**d)
        #             user.save()
        #             dic = {'tip':'注册成功'}
        #             return redirect(reverse('login'))
        # return HttpResponse('注册不成功')


def login_views(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request,'login.html', {'form':form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username,password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect('/')
            else:
                msg = {'msg':'Wrong password'}
                return render(request,'login.html', locals())
        else:
            return render(request,'login.html',locals())


def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect('/')



def changepwd_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            print('-----')
            #是否是用户名修改密码
            user = User.objects.filter(username__exact=username)
            password = form.cleaned_data['old_password']
            if user:
                #判断密码是否正确
                user = auth.authenticate(username=username, password=password)
            else:
                #是否是邮箱修改密码
                user = User.objects.filter(email__exact=username)
                user = auth.authenticate(username=username, password=password)
            if user and user.is_active:

                new_password = form.cleaned_data['password2']
                user.set_password(new_password)
                user.save()
                #print(new_password)
                return HttpResponseRedirect('/myuser/login/')
            else:
                msg = {'msg':'username or Email does not exsit '}
                return render(request,'changepwd.html', locals())
        else:
            error_msg = form.errors.as_json()
            error_msg = json.dumps(error_msg)
            return render(request,'changepwd.html', locals())
    else:
        form = ChangePasswordForm()
        return render(request,'changepwd.html', locals())


