""" description """
from celery.loaders import app
from django.core import mail


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
    for notice in Notice.objects.filter(status=1):
        if notice.celery_status == 'ABORT':
            notice.cid = cid
            notice.send()
    connection.close()
