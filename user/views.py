from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import viewsets
from django.views.generic import TemplateView
from django.template.response import TemplateResponse
from user.serializers import UserSerializer
from django.http.response import HttpResponse
from django.shortcuts import redirect,reverse
from django.contrib.auth import login,logout,authenticate


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginView(TemplateView):
    template_name = 'login.html'


class RegisterView(TemplateView):
    template_name = 'register.html'

    def post(self,request,*args,**kwargs):
        print(request.POST.get('user'))
        context = self.get_context_data(*args,**kwargs)
        return self.render_to_response(context)


def login_view(request):
    response = TemplateResponse(request, 'login.html')
    return response


def register_view(request):
    if request.method == 'GET':
        return render(request,'register.html')
    elif request.method == 'POST':
        user = request.POST.get('user', '')
        passwd1 =request.POST.get('passwd1', '')
        passwd2 =request.POST.get('passwd2', '')
        email = request.POST.get('email','')
        if passwd1 == passwd2:
            if not User.objects.filter(username=user):
                d = dict(username=user, password=passwd1, is_staff=1, is_superuser=1,email=email)
                user = User.objects.create_user(**d)
                user.save()
                dic = {'tip':'注册成功'}
                return redirect(reverse('login'))
    #
    # response = TemplateResponse(request, 'register.html')
    # return response