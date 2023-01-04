from django.contrib import admin
from .models import TestJob


class TestJobAdmin(admin.ModelAdmin):
    list_display = ("model", "pqc", "status", "n_samples")


admin.site.register(TestJob, TestJobAdmin)
