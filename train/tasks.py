from time import sleep
from celery import shared_task

@shared_task()
def train_HAE_model_task(job, lr, epochs, batch_size, n_samples):
    sleep(5)  # Simulate expensive operation(s) that freeze Django
    print("DONE")
    