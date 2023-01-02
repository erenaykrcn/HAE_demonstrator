import os
dirname = os.path.dirname(__file__)

from django.http import HttpResponse, JsonResponse
import plotly.express as px
import plotly
import numpy as np
import pandas as pd

from .models import TrainJob
from .tasks import train_HAE_model_task
from django.forms.models import model_to_dict


def start_training(request):
	lr = 10**int(request.GET["learningRate"])
	epochs = request.GET["epochs"]
	batch_size = request.GET["batchSize"]
	n_samples = request.GET["nSamples"]
	pqc = request.GET["pqc"]
	model = request.GET["model"]

	job = TrainJob.objects.create(epochs=int(epochs),
								  n_samples=int(n_samples),
								  batch_size=int(batch_size),
								  learning_rate=float(lr),
								  pqc=pqc,
								  model=model,
		)
	train_HAE_model_task.delay(model_to_dict(job))

	return HttpResponse(job.id)


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
