from rest_framework import routers

from user.views import UserViewSet
from django.urls import path
from .views import register_view,login_views

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'users', UserViewSet)


urlpatterns = [
    path('login/', login_views, name='login'),
    path('resgister/', register_view, name='register')
]