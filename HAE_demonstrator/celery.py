import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HAE_demonstrator.settings")
app = Celery("HAE_demonstrator")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.control.purge()
