from django.http import HttpResponse, JsonResponse
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

	return JsonResponse(model_to_dict(job))
