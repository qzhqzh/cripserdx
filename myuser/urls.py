from rest_framework import routers

from user.views import UserViewSet
from django.urls import path
from .views import register_view,LoginView

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'users', UserViewSet)


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('resgister/', register_view, name='register')
]