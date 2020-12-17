from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from rest_framework import reverse

from task.models import Task, Notice


def get_common_context(request):
    return {
        'user': request.user
    }

def home_view(request):
    response = TemplateResponse(request, 'home.html', get_common_context(request))
    return response


@login_required(login_url='/admin/login')
def design_crispr_offinder_view(request):
    response = TemplateResponse(request, 'crispr-offinder.html', get_common_context(request))
    return response

#
# @login_required(login_url='/admin/login')
# def design_rpa_view(request):
#     response = TemplateResponse(request, 'design-rpa.html', get_common_context(request))
#     return response


# @login_required(login_url='/admin/login')
# def design_lamp_view(request):
#     response = TemplateResponse(request, 'design-lamp.html', get_common_context(request))
#     return response


def downloads_view(request):
    response = TemplateResponse(request, 'downloads.html', get_common_context(request))
    return response


def faq_view(request):
    response = TemplateResponse(request, 'faq.html', get_common_context(request))
    return response


def protocol_crispr_offinder_view(request):
    response = TemplateResponse(request, 'protocol-crispr-offinder.html', get_common_context(request))
    return response

#
# def protocol_rpa_view(request):
#     response = TemplateResponse(request, 'protocol-rpa.html', get_common_context(request))
#     return response
#
#
# def protocol_lamp_view(request):
#     response = TemplateResponse(request, 'protocol-lamp.html', get_common_context(request))
#     return response


def contact_view(request):
    response = TemplateResponse(request, 'contact.html', get_common_context(request))
    return response


def task_view(request):
    tasks = Task.objects.all()
    notices = Notice.objects.all()
    if not request.user.is_superuser:
        tasks = tasks.filter(submitter=request.user)
    context = get_common_context(request)
    context['tasks'] = tasks
    context['notices'] = notices
    response = TemplateResponse(request, 'tasks.html', context)
    return response

def notice_view(request):
    notices = Notice.objects.all()
    context = get_common_context(request)
    context['notices'] = notices
    response = TemplateResponse(request, 'notices.html', context)
    return response


