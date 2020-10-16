from rest_framework import routers

from auth.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
