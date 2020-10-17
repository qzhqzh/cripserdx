import importlib
import os
import uuid

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template import Template, Context
from django.utils import timezone
from softdelete.models import SoftDeleteObject, SoftDeleteManager, SoftDeleteQuerySet

from config.settings import TEMPLATE_ROOT


class UUIDModel(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class BaseQuerySet(SoftDeleteQuerySet):
    def filter_by_user(self, user):
        return self.model.filter_by_user(self, self.filter, user)


class BaseManager(SoftDeleteManager):
    def get_queryset(self):
        qs = super(SoftDeleteManager, self).get_queryset().filter(deleted_at__isnull=True)
        qs.__class__ = BaseQuerySet
        return qs

    def filter_by_user(self, user):
        return self.get_queryset().filter_by_user(user)


class CoreModel(UUIDModel, SoftDeleteObject):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BaseManager()

    @classmethod
    def filter_by_user(cls, queryset_filter, user):
        if user.is_superuser:
            return queryset_filter()
        elif user.groups.filter(name='salesman').first():
            return queryset_filter(salesman=user)
        else:
            return queryset_filter()


class Notice(CoreModel):
    class StatusChoices(models.IntegerChoices):
        """任务状态"""
        FAIL = -1, 'Error'
        WAITING = 0, 'Waiting'
        RUNNING = 2, 'Running'
        SUCCESS = 3, 'Finish'

    status = models.IntegerField(choices=StatusChoices.choices, default=StatusChoices.WAITING, verbose_name='Notice status')
    started_at = models.DateTimeField(null=True, blank=True, verbose_name='Started at')
    finished_at = models.DateTimeField(null=True, blank=True, verbose_name='Finished at')
    model = models.CharField(max_length=128, blank=True, default='', verbose_name='发送模型')
    model_id = models.CharField(max_length=128, blank=True, null=True, default='', verbose_name='发送模型ID')
    model_method = models.CharField(max_length=64, blank=True, null=True, default='', verbose_name='发送模型方法')
    cid = models.CharField(max_length=128, blank=True, default='', verbose_name='Celery ID')

    class Meta:
        verbose_name = 'Notice list'
        ordering = ('-created_at',)

    @property
    def _model(self):
        module_pos = self.model.rfind('.')
        module = importlib.import_module(self.model[0:module_pos])
        return getattr(getattr(module, 'models'), self.model[module_pos + 1:])

    @property
    def template_params(self):
        return {
            'instance': self._model
        }

    def html_template(self):
        template = os.path.join(TEMPLATE_ROOT, 'email', '%s.html' % self.model_method)
        with open(template, 'r', encoding='utf-8') as f:
            return Template(f.read()).render(Context(self.template_params, autoescape=False))

    @property
    def to(self):
        submitter_email = self._model.objects.get(id=self.model_id).submitter.email
        return [submitter_email]

    @property
    def subject(self):
        return 'Crisperdx Notice'

    def send(self):
        email = EmailMultiAlternatives(subject=self.subject, to=self.to)
        html = self.html_template()
        email.attach_alternative(html, "text/html")
        email.send()


class Task(CoreModel):
    class Meta:
        ordering = ('status',)
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    class StatusChoices(models.IntegerChoices):
        """任务状态"""
        ERROR = -1, 'Error'
        WAITING = 0, 'Waiting'
        RUNNING = 2, 'Running'
        FINISH = 3, 'Finish'

    status = models.IntegerField(choices=StatusChoices.choices, default=StatusChoices.WAITING, verbose_name='Task status')
    cmd = models.CharField(max_length=1024)
    rc = models.IntegerField(null=True)
    msg = models.CharField(max_length=10240)
    submitter = models.ForeignKey(User, on_delete=models.CASCADE)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def run(self):
        Notice.objects.create(model='Task', model_id=str(self.id), model_method='run')



    # def __str__(self):
    #     return '%s-%s-%s' % (self.model, self.model_id, self.model_method)
    #
    # @property
    # def celery_status(self):
    #     if self.status == 2:
    #         return 'SUCCESS'
    #     if not self.cid:
    #         return 'NO SUBMIT'
    #     status = AsyncResult(self.cid).status
    #     if status != 'SUCCESS' and self.start_at and utc_now().timestamp() - self.start_at.timestamp() > 300:
    #         return 'ABORT'
    #     return status
    #

    #
    # @classmethod
    # def new_msg(cls, model, method, **params):
    #     kwargs = {
    #         'content_object': model,
    #         'model_method': method,
    #         'params': params
    #     }
    #     cls.objects.create(**kwargs)
    #
    # def send(self):
    #     try:
    #         if hasattr(self.content_object, self.model_method):
    #             self.start()
    #             getattr(self.content_object, self.model_method)(**self.params)
    #             self.finish()
    #         else:
    #             raise Exception('method "%s" not found in model "%s"' % (self.model_method, str(self.content_type)))
    #     except Exception as e:
    #         self.fail(e)
    #
    # def start(self):
    #     self.status = 1
    #     self.start_at = utc_now()
    #     self.save()
    #
    # def finish(self):
    #     self.status = 2
    #     self.start_at = utc_now()
    #     self.save()
    #
    # def fail(self, msg):
    #     self.status = -1
    #     self.finished_at = utc_now()
    #     self.error_log = msg
    #     self.save()
    #     return False
