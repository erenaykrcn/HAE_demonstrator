import os
dirname = os.path.dirname(__file__)

from celery import shared_task
import numpy as np
from .models import CustomPQCJob
from train.models import ActiveTask


import sys
sys.path.append(os.path.join(dirname, '../../HAE/modules/'))
from qnn.utils import sim_expr, meyer_wallach_measure, PQC


@shared_task(bind=True)
def custom_pqc_task(self, job):
	active_task = ActiveTask.objects.all()[0]
	active_task.celery_task_id = self.request.id
	active_task.task_type = "train"
	active_task.task_id = job["id"]
	active_task.save()

	job = CustomPQCJob.objects.get(id=job["id"])

	layers = []
	encoder_entanglement = job.encoder_entanglement
	if "[" in job.encoder_entanglement:
		# Assumes that an entangler map was provided instead of the choices of 
		# full, linear, reverse_linear, pairwise, circular or sca
		encoder_entanglement = job.encoder_entanglement[1:]
		encoder_entanglement = encoder_entanglement[:-2]
		encoder_entanglement = encoder_entanglement.split("],")
		for i, layer in enumerate(encoder_entanglement):
			layer=layer[1:]
			if i == len(encoder_entanglement) - 1:
				layer = layer[:-1]
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
	ansatz_entanglement = job.ansatz_entanglement
	if "[" in job.ansatz_entanglement:
		# Assumes that an entangler map was provided instead of the choices of 
		# full, linear, reverse_linear, pairwise, circular or sca
		ansatz_entanglement = job.ansatz_entanglement[1:]
		ansatz_entanglement = ansatz_entanglement[:-2]
		ansatz_entanglement = ansatz_entanglement.split("],")
		for i, layer in enumerate(ansatz_entanglement):
			layer=layer[1:]
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
			"encoder": job.encoder,
			"ansatz": job.ansatz,
			"encoder_params": {
				"entanglement": encoder_entanglement,
				"alpha": job.encoder_alpha,
				"paulis": [el.replace("[", "").replace("]", "").replace("'", "").replace("\"", "").replace("`", "").replace(" ", "") for el in job.encoder_paulis.split(",")],
				"reps": job.encoder_reps,
				"rotation_blocks": [el.replace("[", "").replace("]", "").replace("'", "").replace("\"", "").replace("`", "").replace(" ", "") for el in job.encoder_rotation_blocks.split(",")],
				"entanglement_blocks": [el.replace("[", "").replace("]", "").replace("'", "").replace("\"", "").replace("`", "").replace(" ", "") for el in job.encoder_entanglement_blocks.split(",")],
				"skip_final_rotation_layer": job.encoder_skip_final_rotation_layer,
			},
			"ansatz_params": {
				"entanglement": ansatz_entanglement,
				"skip_final_rotation_layer": job.ansatz_skip_final_rotation_layer,
				"reps": job.ansatz_reps,
				"rotation_blocks": [el.replace("[", "").replace("]", "").replace("'", "").replace("\"", "").replace("`", "").replace(" ", "") for el in job.ansatz_rotation_blocks.split(",")],
				"entanglement_blocks": [el.replace("[", "").replace("]", "").replace("'", "").replace("\"", "").replace("`", "").replace(" ", "") for el in job.ansatz_entanglement_blocks.split(",")],
				"su2_gates": [el.replace("[", "").replace("]", "").replace("'", "").replace("\"", "").replace("`", "").replace(" ", "") for el in job.ansatz_su2_gates.split(",")],
				"skip_unentangled_qubits": job.ansatz_skip_unentangled_qubits,
			},
	}


	kl_div = sim_expr(custom_qc=custom_dict, path_custom=os.path.join(dirname, f"../static/customs/hist/hist_{job.id}.png"))
	mw_meas = meyer_wallach_measure(custom_qc=custom_dict)

	job.kl_div = round(kl_div, 3)
	job.mw_meas = str(round(mw_meas.real, 3) + round(mw_meas.imag, 3) * 1j)
	job.path_hist = os.path.join(dirname, f"../static/customs/hist/hist_{job.id}.png")

	pqc = PQC(custom_qc=custom_dict)
	pqc.draw(path=os.path.join(dirname, f"../static/customs/qc_images/qc_images_{job.id}.png"))

	job.path_qc_image = os.path.join(dirname, f"../static/customs/qc_images/qc_images_{job.id}.png")
	job.status = "completed"
	job.save()

    