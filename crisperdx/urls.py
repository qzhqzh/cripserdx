from django.urls import path
from rest_framework import routers

from crisperdx.views import (
    home_view,
    downloads_view,
    faq_view,
    contact_view,
    task_view,
    notice_view,
    design_crispr_offinder_view,
    protocol_crispr_offinder_view,
    SettingViewSet, setting_view,
)


router = routers.SimpleRouter(trailing_slash=False)
router.register(r'settings', SettingViewSet, basename='setting')

urlpatterns = router.urls + [
    path('home', home_view, name='home'),
    path('design-crispr-offinder', design_crispr_offinder_view, name='design-crispr-offinder'),
    path('downloads', downloads_view, name='downloads'),
    path('faq', faq_view, name='faq'),
    path('protocol-crispr-offinder', protocol_crispr_offinder_view, name='protocol-crispr-offinder'),
    path('contact', contact_view, name='contact'),

    path('task', task_view, name='task'),
    path('setting', setting_view, name='setting'),
    path('notice', notice_view, name='notice'),
    # path('login', login_view, name='login'),
    # path('resgister',register_view, name='register')
]
