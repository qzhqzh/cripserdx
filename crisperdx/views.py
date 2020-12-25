
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from rest_framework.viewsets import ModelViewSet

from crisperdx.models import Setting
from crisperdx.serializers import SettingSerializer
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
    from django.core.paginator import Paginator

    tasks = Task.objects.all()
    if not request.user.is_superuser:
        tasks = tasks.filter(submitter=request.user)
    context = get_common_context(request)
    context['tasks'] = tasks

    pageIndex = request.GET.get("pageIndex", 0)
    limit = 5
    paginator = Paginator(tasks, limit)
    number = pageIndex
    if int(pageIndex) < 1:
        """当第一页的时候需要处理页码"""
        pageIndex = 1
        number = 0
    page = paginator.page(int(pageIndex))
    DataList = []
    for r in page.object_list:
        DataList.append(r)

    context.update({
        'DataList': DataList,  # 数据列表
        "count": tasks.count(),  # 这里可以是AccountBooks.count()也可以是page.count(),
        "page": page,  # page object
        "number": number,  # 页码
        "limit": limit,  # 每页多少条数据
    })
    response = TemplateResponse(request, 'tasks.html', context)
    return response


def setting_view(request):
    Settings = Setting.objects.all()
    context = get_common_context(request)
    context['settings'] = []
    if request.user.is_superuser:
        context['settings'] = Settings
    response = TemplateResponse(request, 'settings.html', context)
    return response


def notice_view(request):
    from django.core.paginator import Paginator

    notices = Notice.objects.all()
    if not request.user.is_superuser:
        notices = notices.filter(submitter=request.user)
    context = get_common_context(request)
    context['notices'] = notices

    pageIndex = request.GET.get("pageIndex", 0)
    limit = 5
    paginator = Paginator(notices, limit)
    number = pageIndex
    if int(pageIndex) < 1:
        """当第一页的时候需要处理页码"""
        pageIndex = 1
        number = 0
    page = paginator.page(int(pageIndex))
    DataList = []
    for r in page.object_list:
        DataList.append(r)

    context.update({
        'DataList': DataList,  # 数据列表
        "count": notices.count(),  # 这里可以是AccountBooks.count()也可以是page.count(),
        "page": page,  # page object
        "number": number,  # 页码
        "limit": limit,  # 每页多少条数据
    })

    response = TemplateResponse(request, 'notices.html', context)
    return response


class SettingViewSet(ModelViewSet):
    """配置系统的默认变量"""
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer

