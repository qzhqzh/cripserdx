from django.shortcuts import redirect,reverse
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http.response import HttpResponse, HttpResponseRedirect
from .form import RegisterForm
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


class LoginView(TemplateView):
    template_name = 'login.html'