from django.urls import path
from custom_pqc.views import custom_start, custom_check


urlpatterns = [
    path("start/", custom_start),
    path("check/", custom_check),
]