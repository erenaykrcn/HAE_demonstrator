from django.db import models


class CustomPQCJob(models.Model):
	status = models.CharField(max_length=15,
                  choices=(
                  	("pending", "pending"),
                  	("completed", "completed"),
                  	("failed", "failed")),
                  default="pending")
	encoder = models.CharField(max_length=30,
                  choices=(
                  	("ZFeatureMap", "ZFeatureMap"),
                  	("ZZFeatureMap", "ZZFeatureMap"),
                  	("PauliFeatureMap", "PauliFeatureMap"),
                  	("NLocal", "NLocal"),
                  	),
                  default="ZFeatureMap")
	ansatz = models.CharField(max_length=30,
                  choices=(
                  	("RealAmplitudes", "RealAmplitudes"),
                  	("EfficientSU2", "EfficientSU2"),
                  	("TwoLocal", "TwoLocal"),
                  	),
                  default="RealAmplitudes")

	encoder_reps = models.IntegerField(default=2, blank=True, null=True)
	encoder_entanglement = models.TextField(default="full", blank=True, null=True)
	encoder_paulis = models.TextField(default="['Z', 'ZZ']", blank=True, null=True)
	encoder_alpha = models.IntegerField(default=2, blank=True, null=True)
	encoder_rotation_blocks = models.TextField(default="['ry', 'rz']", blank=True, null=True)
	encoder_entanglement_blocks = models.TextField(default="cx", blank=True, null=True)
	encoder_skip_final_rotation_layer = models.BooleanField(default=False, blank=True, null=True)

	ansatz_reps = models.IntegerField(default=2, blank=True, null=True)
	ansatz_entanglement = models.TextField(default="full", blank=True, null=True)
	ansatz_su2_gates = models.TextField(default="['ry', 'y']", blank=True, null=True)
	ansatz_rotation_blocks = models.TextField(default="['ry', 'rz']", blank=True, null=True)
	ansatz_entanglement_blocks = models.TextField(default="cx", blank=True, null=True)
	ansatz_skip_final_rotation_layer = models.BooleanField(default=False, blank=True, null=True)
	ansatz_skip_unentangled_qubits = models.BooleanField(default=False, blank=True, null=True)

	path_qc_image = models.TextField(blank=True, null=True)
	path_hist = models.TextField(blank=True, null=True)
	kl_div = models.FloatField(blank=True, null=True)
	mw_meas = models.TextField(blank=True, null=True)

	error_message = models.TextField(blank=True, null=True)

