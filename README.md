Python Version Requirement: 3.10
To run the project, you need WSL enabled if you are using Windows and have a Linux distribution installed. 
Before starting the project you should install and start the redis-server on the linux distribution.
Afterwards, you should open up two shells and run:
	"python manage.py runserver"
	"python -m celery -A HAE_demonstrator worker --pool=solo --purge"
after activating the virtual environment respectively.
