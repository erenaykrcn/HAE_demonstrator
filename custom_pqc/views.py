import os
dirname = os.path.dirname(__file__)

from django.http import JsonResponse
from celery import current_task
from HAE_demonstrator.celery import app

from .models import CustomPQCJob
from train.models import ActiveTask
from .tasks import custom_pqc_task
from django.forms.models import model_to_dict


def custom_start(request):
	encoder = request.GET["encoder"]
	ansatz = request.GET["ansatz"]
	job = CustomPQCJob.objects.create(
		encoder=encoder, ansatz=ansatz,
		encoder_reps=request.GET["encoder_reps"],
		encoder_entanglement = request.GET["encoder_entanglement"] if "encoder_entanglement" in request.GET.keys() else None,
		encoder_paulis = request.GET["encoder_paulis"] if "encoder_paulis" in request.GET.keys() else None,
		encoder_alpha = request.GET["encoder_alpha"] if "encoder_alpha" in request.GET.keys() else None,
		encoder_rotation_blocks =request.GET["encoder_rotation_blocks"] if "encoder_rotation_blocks" in request.GET.keys() else None,
		encoder_entanglement_blocks = request.GET["encoder_entanglement_blocks"] if "encoder_entanglement_blocks" in request.GET.keys() else None,
		encoder_skip_final_rotation_layer = request.GET["encoder_skip_final_rotation_layer"] if "encoder_skip_final_rotation_layer" in request.GET.keys() else None,

		ansatz_reps = request.GET["ansatz_reps"] if "ansatz_reps" in request.GET.keys() else None,
		ansatz_entanglement = request.GET["ansatz_entanglement"] if "ansatz_entanglement" in request.GET.keys() else None,
		ansatz_su2_gates = request.GET["ansatz_su2_gates"] if "ansatz_su2_gates" in request.GET.keys() else None,
		ansatz_rotation_blocks = request.GET["ansatz_rotation_blocks"] if "ansatz_rotation_blocks" in request.GET.keys() else None,
		ansatz_entanglement_blocks = request.GET["ansatz_entanglement_blocks"] if "ansatz_entanglement_blocks" in request.GET.keys() else None,
		ansatz_skip_final_rotation_layer = request.GET["ansatz_skip_final_rotation_layer"] if "ansatz_skip_final_rotation_layer" in request.GET.keys() else None,
		ansatz_skip_unentangled_qubits = request.GET["ansatz_skip_unentangled_qubits"] if "ansatz_skip_unentangled_qubits" in request.GET.keys() else None,
		)
	
	# Terminate the current ongoing task- if there is any
	active_task = ActiveTask.objects.all()[0]
	app.control.revoke(active_task.celery_task_id, terminate=True)

	custom_pqc_task.delay(model_to_dict(job))
	return JsonResponse(model_to_dict(job))


def custom_check(request):
    job_id = request.GET["job_id"]
    job = CustomPQCJob.objects.get(id=job_id)
    return JsonResponse(model_to_dict(job))
