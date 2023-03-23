import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
# variable for the Celery command-line program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

app = Celery('myshop') # create an instance of the application

# We load any custom configuration from our project settings using the config_from_object() method. The namespace attribute specifies the prefix that Celery-related settings will have in our settings.py file. By setting the CELERY namespace, all Celery settings need to include the CELERY_ prefix in their name (for example, CELERY_BROKER_URL).
app.config_from_object('django.conf:settings', namespace='CELERY')

# tell Celery to auto-discover asynchronous tasks for our applications. Celery will look for a tasks.py file in each application directory of apps added to INSTALLED_APPS in order to load asynchronous tasks defined in it.
app.autodiscover_tasks()



# Everything you execute in a view affects response times. In many situations, you might want to return a response to the user as quickly as possible and let the server execute some process asynchronously. This is especially relevant for time-consuming processes or processes subject to failure, which might need a retry policy. For example, a video sharing platform allows users to upload videos but requires a long time to transcode uploaded videos. The site might return a response to users to inform them that the transcoding will start soon, and start transcoding the video asynchronously. Another example is sending emails to users. If your site sends email notifications from a view, the SMTP connection might fail or slow down the response. Launching asynchronous tasks is essential to avoid blocking the code execution.

# Celery is a distributed task queue that can process vast amounts of messages. It does real-time processing but also supports task scheduling. Using Celery, not only can you create asynchronous tasks easily and let them be executed by workers as soon as possible, but you can also schedule them to run at a specific time.

# Celery requires a message broker in order to handle requests from an external source. The broker takes care of sending messages to Celery workers, which process tasks as they receive them.
# There are several options to choose as a message broker for Celery, including key/value stores such as Redis, or an actual message system such as RabbitMQ
