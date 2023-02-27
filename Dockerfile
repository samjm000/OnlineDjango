# pull official base image
FROM python:3.10.10

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# installs
RUN  pip install psycopg2 
RUN  pip install --upgrade pip

# install dependencies
COPY ./requirements.txt .
RUN pip install farm-haystack
RUN pip install -r requirements.txt

# copy project
COPY . .

# collect static files
RUN python manage.py collectstatic --noinput

# add and run as non-root user
RUN adduser -D myuser
USER myuser

# run gunicorn
CMD gunicorn onlinekai.wsgi:application --bind 0.0.0.0:$PORT