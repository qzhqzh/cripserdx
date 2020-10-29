from __future__ import absolute_import, unicode_literals

import os

from celery import Celery, platforms, Task
from django.core import mail

from config.funcs import utc_now

platforms.C_FORCE_ROOT = True  # 加上这一行

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@app.task(max_retries=3, time_limit=3 * 24 * 60 * 60, )
def run_task(task):
    from task.models import Job
    Job(task).run()


@app.task(bind=True)
def notification_service(self):
    from task.models import Notice
    connection = mail.get_connection()
    connection.open()
    cid = str(self.request.id)
    notices = Notice.objects.filter(status=0, cid='')
    notices.update(cid=cid)
    for notice in Notice.objects.filter(cid=cid):
        notice.send()
        notice.started_at = utc_now()
        notice.status = 1
        notice.save()
    for notice in Notice.objects.filter(status=1):
        if notice.celery_status == 'ABORT':
            notice.cid = cid
            notice.send()
        notice.finished_at = utc_now()
        notice.status = 2
        notice.save()
    connection.close()
