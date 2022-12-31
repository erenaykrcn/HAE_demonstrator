from django.urls import path
from train.views import start_training, check_training


urlpatterns = [
    path("start-training/", start_training),
    path("check-training/", check_training),
]