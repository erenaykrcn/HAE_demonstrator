from django.db import models
from custom_pqc.models import CustomPQCJob


class TrainJob(models.Model):
	epochs = models.IntegerField(default="50")
	n_samples = models.IntegerField(default="100")
	batch_size = models.IntegerField(default="32")
	learning_rate = models.FloatField(default=1e-3)

	is_binary = models.BooleanField(default=True)
	initial_point = models.TextField(blank=True, null=True)
	max_iter = models.IntegerField(default=100)

	status = models.CharField(max_length=15,
                  choices=(
                  	("pending", "pending"),
                  	("completed", "completed"),
                  	("failed", "failed")),
                  default="pending")

	result_path = models.TextField(null=True, blank=True)
	loss_string = models.TextField(null=True, blank=True)
	model = models.CharField(
		choices=(
                  	("HAE", "HAE"),
                  	("QVC", "QVC"),
                ),
		default="HAE",
		max_length=15,
		)
	pqc = models.TextField(default="1")
	customCircuitJob = models.ForeignKey(CustomPQCJob, on_delete=models.CASCADE, blank=True, null=True)

