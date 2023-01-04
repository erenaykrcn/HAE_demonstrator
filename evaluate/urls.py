from django.urls import path
from evaluate.views import evaluate_metric, evaluate_metric_check


urlpatterns = [
    path("metric/", evaluate_metric),
    path("metric-check/", evaluate_metric_check),
]