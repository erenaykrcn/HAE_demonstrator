from django.contrib import admin
from .models import TrainJob, ActiveTask


class TrainJobAdmin(admin.ModelAdmin):
    list_display = ("model", "pqc", "status", "epochs")


class ActiveTaskAdmin(admin.ModelAdmin):
    list_display = ("celery_task_id", "task_type",)


admin.site.register(TrainJob, TrainJobAdmin)
admin.site.register(ActiveTask, ActiveTaskAdmin)
