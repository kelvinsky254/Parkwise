"""
Celery application for Parkwise.
Loaded via parkwise/__init__.py so it's available as soon as Django starts.
"""

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "parkwise.settings.dev")

app = Celery("parkwise")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")