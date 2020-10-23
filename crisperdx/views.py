from django.template.response import TemplateResponse

from task.models import Task


def home_view(request):
    response = TemplateResponse(request, 'home.html', {})
    return response


def design_pcr_view(request):
    response = TemplateResponse(request, 'design-pcr.html', {})
    return response


def design_rpa_view(request):
    response = TemplateResponse(request, 'design-rpa.html', {})
    return response


def design_lamp_view(request):
    response = TemplateResponse(request, 'design-lamp.html', {})
    return response


def downloads_view(request):
    response = TemplateResponse(request, 'downloads.html', {})
    return response


def faq_view(request):
    response = TemplateResponse(request, 'faq.html', {})
    return response


def protocol_pcr_view(request):
    response = TemplateResponse(request, 'protocol-pcr.html', {})
    return response


def protocol_rpa_view(request):
    response = TemplateResponse(request, 'protocol-rpa.html', {})
    return response


def protocol_lamp_view(request):
    response = TemplateResponse(request, 'protocol-lamp.html', {})
    return response


def contact_view(request):
    response = TemplateResponse(request, 'contact.html', {})
    return response


def task_view(request):
    tasks = Task.objects.all()
    if not request.user.is_superuser:
        tasks = tasks.filter(submitter=request.user)
    response = TemplateResponse(request, 'tasks.html', {'tasks': tasks})
    return response
