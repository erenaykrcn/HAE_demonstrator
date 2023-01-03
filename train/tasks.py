import os
dirname = os.path.dirname(__file__)

from celery import shared_task
from celery.bin import amqp
import numpy as np
from .models import TrainJob

import sys

sys.path.append(os.path.join(dirname, '../../HAE/modules/'))
from HAE.HAE import HAE
from QVC_autoencoder.QVC_autoencoder import QVCAutoencoder
from qnn.qcircuits.circuit_map import N_PARAMS


@shared_task()
def train_model_task(job):
	model = job["model"]
	pqc = int(job["pqc"])
	n_samples = int(job["n_samples"])

	if model == "HAE":
		learningRate = float(job["learning_rate"])
		batchSize = int(job["batch_size"])
		epochs = int(job["epochs"])
		model = HAE(qc_index=pqc, epochs=epochs, batchSize=batchSize, learningRate=learningRate, n_samples=n_samples)
		result_path = model.trainReconstruction(job)
	elif model == "QVC":
		max_iter = job["max_iter"]
		is_binary = bool(job["is_binary"])
		initial_point = job["initial_point"] if job["initial_point"] else np.random.random(N_PARAMS[pqc])

		model = QVCAutoencoder(qc_index=pqc, max_iter=max_iter, n_samples=n_samples, job=job)
		result_path = model.train(initial_point=initial_point, is_binary=is_binary)
	
	train_job = TrainJob.objects.get(id=job["id"])
	train_job.result_path = result_path
	train_job.status = "completed"
	train_job.save()

    