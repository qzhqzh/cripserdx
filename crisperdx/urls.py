from django.urls import path

from crisperdx.views import home_view, design_view, downloads_view, faq_view, protocol_view, contact_view

urlpatterns = [
    path('home', home_view, name='home'),
    path('design', design_view, name='design'),
    path('downloads', downloads_view, name='downloads'),
    path('faq', faq_view, name='faq'),
    path('protocol', protocol_view, name='protocol'),
    path('contact', contact_view, name='contact'),
]
