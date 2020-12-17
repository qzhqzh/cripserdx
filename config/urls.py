"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from user.urls import router as auth_router
# from auth.urls import router as auth_router
from task.urls import router as task_router
import crisperdx.urls
import myuser.urls

from crisperdx.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/', include(auth_router.urls)),
    path('task/', include(task_router.urls)),
    path('api-user/', include('rest_framework.urls', namespace='rest_framework')),
    # path('user/', include(auth_router.urls)),
    path('myuser/', include('myuser.urls')),

    # not very good
    path('', include(crisperdx.urls)),
    path('', home_view, name='home'),
]
