import os
dirname = os.path.dirname(__file__)

from django.http import HttpResponse, JsonResponse
import plotly.express as px
import plotly
import numpy as np
import pandas as pd

from .models import TrainJob
from custom_pqc.models import CustomPQCJob
from .tasks import train_model_task
from django.forms.models import model_to_dict


def start_training(request):
	if request.GET["model"] == "HAE":
		lr = 10**int(request.GET["learningRate"])
		epochs = request.GET["epochs"]
		batch_size = request.GET["batchSize"]
		n_samples = request.GET["nSamples"]

		if "pqc" in request.GET.keys():
			pqc = request.GET["pqc"]
			job = TrainJob.objects.create(epochs=int(epochs),
										  n_samples=int(n_samples),
										  batch_size=int(batch_size),
										  learning_rate=float(lr),
										  pqc=pqc,
										  model="HAE",
				)
		elif "jobId" in request.GET.keys():
			customJobId = request.GET["jobId"]
			job = TrainJob.objects.create(epochs=int(epochs),
										  n_samples=int(n_samples),
										  batch_size=int(batch_size),
										  learning_rate=float(lr),
										  customCircuitJob=CustomPQCJob.objects.get(id=customJobId),
										  model="HAE",
				)

	elif request.GET["model"] == "QVC":
		max_iter = request.GET["max_iter"]
		n_samples = request.GET["nSamples"]
		is_binary = request.GET["classification"] == "binary"
		initial_point = request.GET["initial_point"]

		if "pqc" in request.GET.keys():
			pqc = request.GET["pqc"]
			job = TrainJob.objects.create(max_iter=int(max_iter),
										  n_samples=int(n_samples),
										  is_binary=is_binary,
										  initial_point=None if initial_point=="random" else initial_point,
										  pqc=pqc,
										  model="QVC",
				)
		elif "jobId" in request.GET.keys():
			customJobId = request.GET["jobId"]
			job = TrainJob.objects.create(max_iter=int(max_iter),
										  n_samples=int(n_samples),
										  is_binary=is_binary,
										  initial_point=None if initial_point=="random" else initial_point,
										  customCircuitJob=CustomPQCJob.objects.get(id=customJobId),
										  model="QVC",
				)

	custom_dict = {}
	if "jobId" in request.GET.keys():
		customCircuitJob = CustomPQCJob.objects.get(id=customJobId)
		custom_dict = {
				"encoder": customCircuitJob.encoder,
				"ansatz": customCircuitJob.ansatz,
				"encoder_params": {
					"entanglement": customCircuitJob.encoder_entanglement,
					"alpha": customCircuitJob.encoder_alpha,
					"paulis": [el.replace("[", "").replace("]", "").replace("'", "").replace("\"", "").replace("`", "").replace(" ", "") for el in customCircuitJob.encoder_paulis.split(",")],
					"reps": customCircuitJob.encoder_reps,
					"rotation_blocks": [el.replace("[", "").replace("]", "").replace("'", "").replace("\"", "").replace("`", "").replace(" ", "") for el in customCircuitJob.encoder_rotation_blocks.split(",")],
					"entanglement_blocks": [el.replace("[", "").replace("]", "").replace("'", "").replace("\"", "").replace("`", "").replace(" ", "") for el in customCircuitJob.encoder_entanglement_blocks.split(",")],
					"skip_final_rotation_layer": customCircuitJob.encoder_skip_final_rotation_layer,
				},
				"ansatz_params": {
					"entanglement": customCircuitJob.ansatz_entanglement,
					"skip_final_rotation_layer": customCircuitJob.ansatz_skip_final_rotation_layer,
					"reps": customCircuitJob.ansatz_reps,
					"rotation_blocks": [el.replace("[", "").replace("]", "").replace("'", "").replace("\"", "").replace("`", "").replace(" ", "") for el in customCircuitJob.ansatz_rotation_blocks.split(",")],
					"entanglement_blocks": [el.replace("[", "").replace("]", "").replace("'", "").replace("\"", "").replace("`", "").replace(" ", "") for el in customCircuitJob.ansatz_entanglement_blocks.split(",")],
					"su2_gates": [el.replace("[", "").replace("]", "").replace("'", "").replace("\"", "").replace("`", "").replace(" ", "") for el in customCircuitJob.ansatz_su2_gates.split(",")],
					"skip_unentangled_qubits": customCircuitJob.ansatz_skip_unentangled_qubits,
				},
		}


	train_model_task.delay(job=model_to_dict(job), custom_dict=custom_dict)
	dic = model_to_dict(job)
	return JsonResponse(dic)


def check_training(request):
	job_id = request.GET["job_id"]
	job = TrainJob.objects.get(id=job_id)
	loss_string = job.loss_string
	dic = model_to_dict(job)

	if loss_string:
		loss = []
		loss_list = loss_string.split(";")[:-1]
		for item in loss_list:
			loss.append(float(item))

		epochs = []
		for i in range(len(loss_list)):
			if len(loss_list) > 1:
				path_del = f"../static/train_hae/loss_plot/{job_id}_{i}.png"
				if os.path.exists(os.path.join(dirname, path_del)):
					os.remove(os.path.join(dirname, path_del))
			epochs.append(i+1)
			
		df = pd.DataFrame(dict(
		    epochs = epochs,
		    loss = loss
		))

		fig = px.line(df, x="epochs", y="loss", title='Loss Values')

		path = f"../static/train_hae/loss_plot/{job_id}_{epochs[-1]}.png"
		fig.write_image(os.path.join(dirname, path))
		dic["epoch"] = epochs[-1]

	return JsonResponse(dic)
