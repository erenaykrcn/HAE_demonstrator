import os
dirname = os.path.dirname(__file__)

from celery import shared_task
from celery.bin import amqp
import numpy as np
from .models import TrainJob
from custom_pqc.models import CustomPQCJob

import sys

sys.path.append(os.path.join(dirname, '../../HAE/modules/'))
from HAE.HAE import HAE
from QVC_autoencoder.QVC_autoencoder import QVCAutoencoder
from qnn.qcircuits.circuit_map import N_PARAMS


@shared_task()
def train_model_task(job):
	model = job["model"]
	n_samples = int(job["n_samples"])

	if job["customCircuitJob"]:
		customCircuitJob = CustomPQCJob().objects.get(id=job["customCircuitJob"]["id"])
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
		initial_point = job["initial_point"] if job["initial_point"] else np.random.random(N_PARAMS[pqc])

		if job["pqc"]:
			pqc = int(job["pqc"])
			model = QVCAutoencoder(qc_index=pqc, max_iter=max_iter, n_samples=n_samples, job=job)
		elif job["customCircuitJob"]:
			model = QVCAutoencoder(custom_qc=custom_dict, max_iter=max_iter, n_samples=n_samples, job=job)
			
		result_path = model.train(initial_point=initial_point, is_binary=is_binary)
	
	train_job = TrainJob.objects.get(id=job["id"])
	train_job.result_path = result_path
	train_job.status = "completed"
	train_job.save()

    