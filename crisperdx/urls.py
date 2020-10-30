from django.urls import path

from crisperdx.views import (
    home_view,
    downloads_view,
    design_pcr_view,
    design_rpa_view,
    design_lamp_view,
    faq_view,
    protocol_pcr_view,
    protocol_rpa_view,
    protocol_lamp_view,
    contact_view,
    task_view,
    notice_view,
)
from task.views import TaskViewSet

urlpatterns = [
    path('home', home_view, name='home'),
    path('design-pcr', design_pcr_view, name='design-pcr'),
    path('design-rpa', design_rpa_view, name='design-rpa'),
    path('design-lamp', design_lamp_view, name='design-lamp'),
    path('downloads', downloads_view, name='downloads'),
    path('faq', faq_view, name='faq'),
    path('protocol-pcr', protocol_pcr_view, name='protocol-pcr'),
    path('protocol-rpa', protocol_rpa_view, name='protocol-rpa'),
    path('protocol-lamp', protocol_lamp_view, name='protocol-lamp'),
    path('contact', contact_view, name='contact'),

    path('task', task_view, name='task'),
    path('notice', notice_view, name='notice'),
    # path('login', login_view, name='login'),
    # path('resgister',register_view, name='register')
]
