from django.db import models
from custom_pqc.models import CustomPQCJob


class TestJob(models.Model):
	n_samples = models.IntegerField(default=200)
	is_binary = models.BooleanField(default=True)

	status = models.CharField(max_length=15,
                  choices=(
                  	("pending", "pending"),
                  	("completed", "completed"),
                  	("failed", "failed")),
                  default="pending")

	result_path = models.TextField(null=True, blank=True)
	model = models.CharField(
		choices=(
                  	("HAE", "HAE"),
                  	("QVC", "QVC"),
                ),
		default="HAE",
		max_length=15,
		)
	pqc = models.TextField(null=True, blank=True)
	customCircuitJob = models.ForeignKey(CustomPQCJob, on_delete=models.CASCADE, blank=True, null=True)

	precision = models.FloatField(null=True, blank=True)
	recall = models.FloatField(null=True, blank=True)
	f1 = models.FloatField(null=True, blank=True)

	precision_cl = models.FloatField(null=True, blank=True)
	recall_cl = models.FloatField(null=True, blank=True)
	f1_cl = models.FloatField(null=True, blank=True)
