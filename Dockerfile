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

EXPOSE 8000

CMD ["manage.py", "runserver", "0.0.0.0:8000"]