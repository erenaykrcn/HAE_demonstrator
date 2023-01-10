import os
dirname = os.path.dirname(__file__)

from celery import shared_task
import numpy as np
from .models import TestJob
from train.models import ActiveTask

import sys
sys.path.append(os.path.join(dirname, '../../HAE/modules/'))
from metrics.metrics import get_scores
from metrics.predict import predict_HAE, predict_classical, predict_QVC
from preprocessing.visualize import plot_PCA_2D


@shared_task(bind=True)
def test_model_task(self, job, test_data, test_labels, path_save="", custom_dict={}):
	active_task = ActiveTask.objects.all()[0]
	active_task.celery_task_id = self.request.id
	active_task.task_type = "train"
	active_task.task_id = job["id"]
	active_task.save()

	model = job["model"]
	pqc = int(job["pqc"]) if job["pqc"] else 0
	n_samples = int(job["n_samples"])
	test_job = TestJob.objects.get(id=job["id"])
	predict_cl, labels_cl = predict_classical(test_data=test_data, test_labels=test_labels)

	if model == "HAE":
		predict, labels = predict_HAE(qc_index=pqc, path=test_job.result_path, test_data=test_data, test_labels=test_labels, custom_dict=custom_dict)
	elif model == "QVC":
		predict, labels = predict_QVC(qc_index=pqc, path=test_job.result_path, test_data=test_data, test_labels=test_labels, custom_dict=custom_dict)

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

	if path_save:
		labels = np.array(labels)
		predict = np.array(predict)
		correctly_discovered_anomalies = np.where((labels == predict) & (labels==-1))
		wrongly_discovered_anomalies = np.where((labels != predict) & (labels==1))

		labels[correctly_discovered_anomalies] = 2
		labels[wrongly_discovered_anomalies] = -2
		plot_PCA_2D(test_data=test_data, test_labels=labels, path_save=path_save)

    