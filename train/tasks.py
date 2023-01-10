import os
dirname = os.path.dirname(__file__)

from celery import shared_task
import numpy as np
from .models import TrainJob, ActiveTask
from custom_pqc.models import CustomPQCJob

import sys

sys.path.append(os.path.join(dirname, '../../HAE/modules/'))
from HAE.HAE import HAE
from QVC_autoencoder.QVC_autoencoder import QVCAutoencoder
from qnn.qcircuits.circuit_map import N_PARAMS
from qnn.utils import PQC


@shared_task(bind=True)
def train_model_task(self, job, custom_dict={}):
	model = job["model"]
	n_samples = int(job["n_samples"])

	active_task = ActiveTask.objects.all()[0]
	active_task.celery_task_id = self.request.id
	active_task.task_type = "train"
	active_task.task_id = job["id"]
	active_task.save()

	if model == "HAE":
		learningRate = float(job["learning_rate"])
		batchSize = int(job["batch_size"])
		epochs = int(job["epochs"])

		if job["pqc"]:
			pqc = int(job["pqc"])
			model = HAE(qc_index=pqc, epochs=epochs, batchSize=batchSize, learningRate=learningRate, n_samples=n_samples)
		elif job["customCircuitJob"]:
			model = HAE(custom_qc=custom_dict, epochs=epochs, batchSize=batchSize, learningRate=learningRate, n_samples=n_samples)
		result_path = model.trainReconstruction(job)

	elif model == "QVC":
		max_iter = job["max_iter"]
		is_binary = job["is_binary"]
		if job["pqc"]:
			initial_point = job["initial_point"] if job["initial_point"] else np.random.random(N_PARAMS[pqc])
			pqc = int(job["pqc"])
			model = QVCAutoencoder(qc_index=pqc, max_iter=max_iter, n_samples=n_samples, job=job)
		elif job["customCircuitJob"]:
			pqc_model = PQC(custom_qc=custom_dict)
			initial_point = job["initial_point"] if job["initial_point"] else np.random.random(pqc_model.num_parameters)
			model = QVCAutoencoder(custom_qc=custom_dict, max_iter=max_iter, n_samples=n_samples, job=job)
	
		result_path = model.train(initial_point=initial_point, is_binary=is_binary)
	
	train_job = TrainJob.objects.get(id=job["id"])
	train_job.result_path = result_path
	train_job.status = "completed"
	train_job.save()

    