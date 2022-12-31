from django.http import HttpResponse
from .models import TrainJob
from .tasks import train_HAE_model_task


def start_training(request):
	lr = request.GET["learningRate"]
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
	train_HAE_model_task.delay(job, lr, epochs, batch_size, n_samples, model)

	return HttpResponse(batch_size)


def check_training(request):
	return HttpResponse("")
