from rest_framework import routers

from .views import TaskViewSet, NoticeViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'task', TaskViewSet, basename='tasks')
router.register(r'note', NoticeViewSet, basename='notices')
