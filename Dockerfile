FROM python:3.9-alpine
RUN apk add --no-cache mariadb-dev build-base git libffi-dev geos-dev
ADD . /seetree
WORKDIR /seetree
# required for flask commands to work
ENV FLASK_APP=seetree
ENV WORKERS=1
ENV LOG_LEVEL=INFO
RUN pip install -e .
RUN pip install -r /seetree/requirements.txt
CMD gunicorn seetree.app:app --bind 0.0.0.0:5000 --workers $WORKERS --log-level $LOG_LEVEL
