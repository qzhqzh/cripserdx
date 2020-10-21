from django.template.response import TemplateResponse

from task.models import Task


def home_view(request):
    response = TemplateResponse(request, 'home.html', {})
    return response


def design_view(request):
    response = TemplateResponse(request, 'design.html', {})
    return response


def downloads_view(request):
    response = TemplateResponse(request, 'downloads.html', {})
    return response


def faq_view(request):
    response = TemplateResponse(request, 'faq.html', {})
    return response


def protocol_view(request):
    response = TemplateResponse(request, 'protocol.html', {})
    return response


def contact_view(request):
    response = TemplateResponse(request, 'contact.html', {})
    return response


def task_view(request):
    tasks = Task.objects.all()
    response = TemplateResponse(request, 'tasks.html', {'tasks': tasks})
    return response
