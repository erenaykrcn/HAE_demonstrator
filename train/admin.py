from django.contrib import admin
from .models import TrainJob


class TrainJobAdmin(admin.ModelAdmin):
    list_display = ("model", "pqc", "status", "epochs")


admin.site.register(TrainJob, TrainJobAdmin)
