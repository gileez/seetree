# SeeTree Home Exercise
## Completed in 8 hours
- all requested functionalities. Tested both combinations of loading images followed by polygons and vice-a-versa.

## Improvements
- loading images \ polygons can be a lengthy process. the appropriate solution as to not block the backend would be to use
an asyncronous worker (such as Celery) to process the loading tasks. This will require installing Flask-celery, running an instance of
  rabbitMQ as the broker. I was unable to complete this within the time constraint. estimated time required: 1.5 hours
- Flask app is currently serving using the builtin flask web server. I would have liked to pack the app into a container
and serve it using a WSGI complaint web server such as gunicorn.
- Write tests.