import os
dirname = os.path.dirname(__file__)

from celery import shared_task
from .models import TrainJob

import sys
sys.path.append(os.path.join(dirname, '../../HAE/modules/'))
from HAE.HAE import HAE
from QVC_autoencoder.QVC_autoencoder import QVCAutoencoder


@shared_task()
def train_HAE_model_task(job):
	model = job["model"]

	pqc = int(job["pqc"])
	learningRate = float(job["learning_rate"])
	n_samples = int(job["n_samples"])

	if model == "HAE":
		batchSize = int(job["batch_size"])
		epochs = int(job["epochs"])
		model = HAE(qc_index=pqc, epochs=epochs, batchSize=batchSize, learningRate=learningRate, n_samples=n_samples)
		result_path = model.trainReconstruction(job)
	elif model == "QVC":
		max_iter = int(job["max_iter"])
		model = QVCAutoencoder(qc_index=pqc, max_iter=max_iter, n_samples=n_samples)

		# TODO: pass initial point and is_binary
		result_path = model.train(job)
	
	train_job = TrainJob.objects.get(id=job["id"])
	train_job.result_path = result_path
	train_job.status = "completed"
	train_job.save()


    