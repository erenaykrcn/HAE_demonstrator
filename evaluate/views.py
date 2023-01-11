import os
dirname = os.path.dirname(__file__)

from django.http import JsonResponse
from celery import current_task
from HAE_demonstrator.celery import app

from .models import TestJob
from train.models import ActiveTask
from custom_pqc.models import CustomPQCJob
from .tasks import test_model_task
from django.forms.models import model_to_dict

import sys
sys.path.append(os.path.join(dirname, '../../HAE/modules/'))
from preprocessing.preprocessing import sample_test_data
from preprocessing.visualize import plot_PCA_2D


def evaluate_metric(request):
    custom_dict = {}
    if "jobId" in request.GET.keys():
        customCircuitJob = CustomPQCJob.objects.get(id=request.GET["jobId"])

        layers = []
        encoder_entanglement = customCircuitJob.encoder_entanglement
        if "[" in customCircuitJob.encoder_entanglement:
            # Assumes that an entangler map was provided instead of the choices of 
            # full, linear, reverse_linear, pairwise, circular or sca
            encoder_entanglement = customCircuitJob.encoder_entanglement[1:]
            encoder_entanglement = encoder_entanglement[:-2]
            encoder_entanglement = encoder_entanglement.split("],")
            for i, layer in enumerate(encoder_entanglement):
                layer=layer[1:]
                gates = []
                layer = layer.split("),")
                for j, gate in enumerate(layer):
                    gate = gate[1:]
                    if y == len(layer) - 1:
                        gate = gate[:-1]
                    gate = gate.split(",")
                    gates.append((int(gate[0]), int(gate[1])))
                layers.append(gates)
            encoder_entanglement = layers

        layers = []
        ansatz_entanglement = customCircuitJob.ansatz_entanglement
        if "[" in customCircuitJob.ansatz_entanglement:
            # Assumes that an entangler map was provided instead of the choices of 
            # full, linear, reverse_linear, pairwise, circular or sca
            ansatz_entanglement = customCircuitJob.ansatz_entanglement[1:]
            ansatz_entanglement = ansatz_entanglement[:-2]
            ansatz_entanglement = ansatz_entanglement.split("],")
            for i, layer in enumerate(ansatz_entanglement):
                layer=layer[1:]
                if i == len(ansatz_entanglement) - 1:
                    layer = layer[:-1]
                gates = []
                layer = layer.split("),")
                for j, gate in enumerate(layer):
                    gate = gate[1:]
                    if j == len(layer) - 1:
                        gate = gate[:-1]
                    gate = gate.split(",")
                    gates.append((int(gate[0]), int(gate[1])))
                layers.append(gates)
            ansatz_entanglement = layers
        custom_dict = {
                "encoder": customCircuitJob.encoder,
                "ansatz": customCircuitJob.ansatz,
                "encoder_params": {
                    "entanglement": encoder_entanglement,
                    "alpha": customCircuitJob.encoder_alpha,
                    "paulis": [el.replace("[", "").replace("]", "").replace("'", "").replace("\"", "").replace("`", "").replace(" ", "") for el in customCircuitJob.encoder_paulis.split(",")],
                    "reps": customCircuitJob.encoder_reps,
                    "rotation_blocks": [el.replace("[", "").replace("]", "").replace("'", "").replace("\"", "").replace("`", "").replace(" ", "") for el in customCircuitJob.encoder_rotation_blocks.split(",")],
                    "entanglement_blocks": [el.replace("[", "").replace("]", "").replace("'", "").replace("\"", "").replace("`", "").replace(" ", "") for el in customCircuitJob.encoder_entanglement_blocks.split(",")],
                    "skip_final_rotation_layer": customCircuitJob.encoder_skip_final_rotation_layer,
                },
                "ansatz_params": {
                    "entanglement": ansatz_entanglement,
                    "skip_final_rotation_layer": customCircuitJob.ansatz_skip_final_rotation_layer,
                    "reps": customCircuitJob.ansatz_reps,
                    "rotation_blocks": [el.replace("[", "").replace("]", "").replace("'", "").replace("\"", "").replace("`", "").replace(" ", "") for el in customCircuitJob.ansatz_rotation_blocks.split(",")],
                    "entanglement_blocks": [el.replace("[", "").replace("]", "").replace("'", "").replace("\"", "").replace("`", "").replace(" ", "") for el in customCircuitJob.ansatz_entanglement_blocks.split(",")],
                    "su2_gates": [el.replace("[", "").replace("]", "").replace("'", "").replace("\"", "").replace("`", "").replace(" ", "") for el in customCircuitJob.ansatz_su2_gates.split(",")],
                    "skip_unentangled_qubits": customCircuitJob.ansatz_skip_unentangled_qubits,
                },
        }



    n_samples = int(request.GET["n_samples"])
    filename = request.GET["filename"]
    is_binary = bool(request.GET["is_binary"]) if "is_binary" in request.GET.keys() else True
    test_data, test_labels = sample_test_data(n_samples, True)
    model = request.GET["model"]
    qvc_inner_path = "/binary_cl" if is_binary else "/multi_cl"
    path_save = os.path.join(dirname, f"../static/eval/scatter/{model}_{n_samples}.png")
    path_save_after_training = os.path.join(dirname, f"../static/eval/scatter/{model}_{n_samples}_after_training.png")
    
    test_data_copy = test_data.copy()
    test_labels_copy = test_labels.copy()
    plot_PCA_2D(test_data=test_data_copy, test_labels=test_labels_copy, path_save=path_save)
    
    # Terminate the current ongoing task- if there is any
    active_task = ActiveTask.objects.all()[0]
    app.control.revoke(active_task.celery_task_id, terminate=True)

    if "pqc" in request.GET.keys():
        pqc = int(request.GET["pqc"])
        job = TestJob.objects.create(
            model=model,
            n_samples=n_samples,
            is_binary=is_binary,
            pqc=pqc,
            result_path=os.path.join(dirname, f"../../HAE/data/training_results{'_QVC' if model=='QVC' else ''}/pqc{pqc}{qvc_inner_path if model=='QVC' else ''}/{filename}"),
            )
        test_model_task.delay(model_to_dict(job), test_data=test_data, test_labels=test_labels, path_save=path_save_after_training, custom_dict=custom_dict)
    elif "jobId" in request.GET.keys():
        customJobId = request.GET["jobId"]
        job = TestJob.objects.create(
            model=model,
            n_samples=n_samples,
            is_binary=is_binary,
            customCircuitJob=CustomPQCJob.objects.get(id=customJobId),
            result_path=os.path.join(dirname, f"../../HAE/data/training_results{'_QVC' if model=='QVC' else ''}/{'custom_qc' if model=='HAE' else 'custom'}{qvc_inner_path if model=='QVC' else ''}/{filename}"),
            )
        test_model_task.delay(model_to_dict(job), test_data=test_data, test_labels=test_labels, path_save=path_save_after_training, custom_dict=custom_dict)

    return JsonResponse(model_to_dict(job))


def evaluate_metric_check(request):
    job_id = request.GET["job_id"]
    job = TestJob.objects.get(id=job_id)
    return JsonResponse(model_to_dict(job))
