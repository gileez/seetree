from celery import Celery
import celery
from seetree.config import Config
from seetree.builder import build_app

# initialize a celery app
celery_app = Celery(__name__, broker=Config.CELERY_BROKER_URL)
# build base app to provide context
app = build_app()


# Wrapper function to provide context to tasks
def set_context(celery_app, app):
    celery_app.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app

# Following function call can be used to pass the app context to the celery app
# In this case this seemed like a more cumbersome solution in comparison
# to generating a db session in the worker code
# set_context(celery_app, app)