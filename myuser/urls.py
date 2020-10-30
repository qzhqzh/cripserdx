from rest_framework import routers

from user.views import UserViewSet
from django.urls import path, re_path
from .views import register_view,login_views,logout_view,changepwd_view

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'users', UserViewSet)


urlpatterns = [
    path('login/', login_views, name='login'),
    path('resgister/', register_view, name='register'),
    path('logout/',logout_view, name='logout'),
    path('update/', changepwd_view, name = 'changepwd' )
]