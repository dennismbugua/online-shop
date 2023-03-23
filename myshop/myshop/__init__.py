# import celery
from .celery import app as celery_app


# You need to import the celery module in the __init__.py file of your project to make sure it is loaded when Django starts
