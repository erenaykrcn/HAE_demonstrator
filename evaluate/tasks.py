import os
dirname = os.path.dirname(__file__)

from celery import shared_task
import numpy as np
from .models import TestJob

import sys
sys.path.append(os.path.join(dirname, '../../HAE/modules/'))
from metrics.metrics import get_scores
from metrics.predict import predict_HAE, predict_classical, predict_QVC


@shared_task()
def test_model_task(job, test_data, test_labels):
	model = job["model"]
	pqc = int(job["pqc"])
	n_samples = int(job["n_samples"])
	test_job = TestJob.objects.get(id=job["id"])
	predict_cl, labels_cl = predict_classical(test_data=test_data, test_labels=test_labels)

	if model == "HAE":
		predict, labels = predict_HAE(qc_index=pqc, path=test_job.result_path, test_data=test_data, test_labels=test_labels)
	elif model == "QVC":
		predict, labels = predict_QVC(qc_index=pqc, path=test_job.result_path, test_data=test_data, test_labels=test_labels)
		print(predict)
	
	f1, precision, recall = get_scores(predict, labels)
	f1_cl, precision_cl, recall_cl = get_scores(predict_cl, labels_cl)

	test_job.precision = precision
	test_job.recall = recall
	test_job.f1 = f1

	test_job.precision_cl = precision_cl
	test_job.recall_cl = recall_cl
	test_job.f1_cl = f1_cl

	test_job.status = "completed"
	test_job.save()

    