from django.contrib import admin
from .models import CustomPQCJob


class CustomPQCJobAdmin(admin.ModelAdmin):
    list_display = ("status", )


admin.site.register(CustomPQCJob, CustomPQCJobAdmin)
