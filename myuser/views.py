from random import Random

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.shortcuts import redirect, reverse, get_object_or_404
from django.contrib.auth.models import User
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views.generic import TemplateView
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import auth
from django.views.generic.base import View

from config.settings import EMAIL_HOST_USER
from crisperdx.views import get_common_context
from .form import RegisterForm, LoginForm, ChangePasswordForm,FindPasswordForm
from django.contrib.auth.decorators import login_required
import json

from .serialziers import UserSerializer


class EmailBackend(ModelBackend):
    '''
    重写authenticate方法
    '''

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = User.objects.filter(Q(username=username) | Q(email=username)).first()
        if user and user.is_active:
            if user.check_password(password):
                return user
            return None
        return None


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
        return render(request,'login.html', {'form': form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            print(username)
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            # user = auth.authenticate(username=username, password=password)
            #not pass
            # user2 = auth.authenticate(email=username, password=password)
            #print(user2)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect('/')
            # else:
            #     user = auth.authenticate(email=username, password=password)
            #     if user and user.is_active:
            #         auth.login(request,user)
            # else:
            #     if user2 and user2.is_active:
            #         return HttpResponseRedirect('/')
            #     msg = {'msg':'Wrong password'}
            #     return render(request,'login.html', locals())
        else:
            return render(request,'login.html',locals())


@login_required
def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


@login_required
def changepwd_view(request, pk):
    pk=int(pk)
    print(pk)
    if request.method == 'POST':
        user = get_object_or_404(User, pk=pk)
        form = ChangePasswordForm(request.POST)
        print(form)
        if form.is_valid():
            if user and user.is_active:
                old_password = form.cleaned_data['old_password']
                print(old_password)
                new_password = form.cleaned_data['password2']
                user = auth.authenticate(username=user.username, password=old_password)
                if user and user.is_active:
                    user.set_password(new_password)
                    user.save()
                    return HttpResponseRedirect('/myuser/login/')
                else:
                    msg = {'msg' : ' Old password is wrong'}
                    return render(request,'changepwd.html',locals())
        else:
            msg = form.errors.as_json()
            msg = json.dumps(msg)
            return render(request, 'changepwd.html', locals())
    else:
        form = ChangePasswordForm()
        return render(request,'changepwd.html', locals())


class FindPassword(View):

    def get(self,request):
        form = FindPasswordForm()
        return render(request,'findpassword.html', locals())

    def post(self, request):
        form = FindPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            code = self.random_str()
            from django.core.mail import send_mail
            request.session["code"] = code
            request.session["email"] = email
            request.session.set_expiry(300)
            send_mail('密码找回',
                      '当前验证码为：{}'.format(code),
                      EMAIL_HOST_USER, [email])
            msg = {'msg':'验证码已发送邮箱请查收'}
            print('----')
            return redirect('/myuser/findpwd2/', locals())
        else:
            msg = form.errors.as_json()
            error_msg = json.dumps(msg)
            print(error_msg)
            return render(request, 'findpassword.html', locals())


    def random_str(self, randomlength=4):
        str = ''
        chars = 'abcdefghijklmnopqrstuvwsyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        length = len(chars) - 1
        random = Random()
        for i in range(randomlength):
            str += chars[random.randint(0, length)]
        return str
#
# class FindPassword(View):
#
#     def get(self,request):
#         emil = request.GET.get('username')
#         user = User.objects.filter(email__exact=emil)
#         if user:
#             return render(request,'findpassword.html')
#         else:
#             return render(request, 'findpassword.html',locals())
#
#    def post(self, request):
#         check_code = request.POST.get('myEmail', None)
#         print(check_code)
#         return HttpResponse('ok')
#
#
#
#
class FindPassword2(View):
    def get(self, request):
        print(request.GET.get('msg'))
        return render(request,'findtwo.html',locals())

    def post(self, request):
        vscode = request.POST.get('vscode',None)
        email = request.session.get('email',None)
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        print(password1,password2,email,vscode)

        if vscode and vscode == request.session.get('code') and password2 == password1:
            user = User.objects.filter(email__exact=email).first()
            user.set_password(password1)
            user.save()
            del request.session['code']
            del request.session['email']

            return HttpResponseRedirect('/myuser/login/')
        else:
            if vscode == request.session.get('code'):
                msg = {'msg':'两次密码不一致'}
            else:
                msg = {'msg': '验证码已过期'}
            return render(request,'findtwo.html',locals())


def user_view(request):
    """ User info view """
    context = get_common_context(request)
    extra_info = UserSerializer(request.user).data
    context.update(extra_info)
    response = TemplateResponse(request, 'user.html', context)
    return response
