import os
dirname = os.path.dirname(__file__)

from celery import shared_task
import numpy as np
from .models import CustomPQCJob


import sys
sys.path.append(os.path.join(dirname, '../../HAE/modules/'))
from qnn.utils import sim_expr, meyer_wallach_measure, PQC


@shared_task()
def custom_pqc_task(job):
	try:
		job = CustomPQCJob.objects.get(id=job["id"])

		custom_dict = {
			"encoder": job.encoder,
			"ansatz": job.ansatz,
			"encoder_params": {
				"entanglement": job.encoder_entanglement,
				"alpha": job.encoder_alpha,
				"paulis": [el.replace("[", "").replace("]", "").replace("'", "").replace("\"", "").replace("`", "").replace(" ", "") for el in job.encoder_paulis.split(",")],
				"reps": job.encoder_reps,
				"rotation_blocks": [el.replace("[", "").replace("]", "").replace("'", "").replace("\"", "").replace("`", "").replace(" ", "") for el in job.encoder_rotation_blocks.split(",")],
				"entanglement_blocks": [el.replace("[", "").replace("]", "").replace("'", "").replace("\"", "").replace("`", "").replace(" ", "") for el in job.encoder_entanglement_blocks.split(",")],
				"skip_final_rotation_layer": job.encoder_skip_final_rotation_layer,
			},
			"ansatz_params": {
				"entanglement": job.ansatz_entanglement,
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

		job.kl_div = kl_div
		job.mw_meas = mw_meas
		job.path_hist = os.path.join(dirname, f"../static/customs/hist/hist_{job.id}.png")

		pqc = PQC(custom_qc=custom_dict)
		pqc.draw(path=os.path.join(dirname, f"../static/customs/qc_images/qc_images_{job.id}.png"))

		job.path_qc_image = os.path.join(dirname, f"../static/customs/qc_images/qc_images_{job.id}.png")
		job.status = "completed"
		job.save()
	except Exception as e:
		job.status = "failed"
		job.error_message = e
		job.save()

    