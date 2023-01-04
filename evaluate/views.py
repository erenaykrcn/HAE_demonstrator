import os
dirname = os.path.dirname(__file__)

from django.http import JsonResponse

from .models import TestJob
from .tasks import test_model_task
from django.forms.models import model_to_dict

import sys
sys.path.append(os.path.join(dirname, '../../HAE/modules/'))
from preprocessing.preprocessing import sample_test_data
from preprocessing.visualize import plot_PCA_2D


def evaluate_metric(request):
    n_samples = int(request.GET["n_samples"])
    pqc = int(request.GET["pqc"])
    filename = request.GET["filename"]
    is_binary = bool(request.GET["is_binary"]) if "is_binary" in request.GET.keys() else True
    test_data, test_labels = sample_test_data(n_samples, True)
    model = request.GET["model"]
    qvc_inner_path = "/binary_cl" if is_binary else "/multi_cl"

    job = TestJob.objects.create(
        model=model,
        n_samples=n_samples,
        is_binary=is_binary,
        pqc=pqc,
        result_path=os.path.join(dirname, f"../../HAE/data/training_results{'_QVC' if model=='QVC' else ''}/pqc{pqc}{qvc_inner_path if model=='QVC' else ''}/{filename}"),
        )
    test_model_task.delay(model_to_dict(job), test_data=test_data, test_labels=test_labels)

    test_data_copy = test_data.copy()
    test_labels_copy = test_labels.copy()
    fig = plot_PCA_2D(test_data=test_data_copy, test_labels=test_labels_copy, path_save=os.path.join(dirname, f"../static/eval/scatter/{model}_{n_samples}.png"))


    return JsonResponse(model_to_dict(job))


def evaluate_metric_check(request):
    job_id = request.GET["job_id"]
    job = TestJob.objects.get(id=job_id)
    return JsonResponse(model_to_dict(job))
