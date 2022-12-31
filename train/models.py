from django.db import models


class TrainJob(models.Model):
	epochs = models.IntegerField(default="50")
	n_samples = models.IntegerField(default="100")
	batch_size = models.IntegerField(default="32")
	learning_rate = models.FloatField(default=1e-3)

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

