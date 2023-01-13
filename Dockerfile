FROM python:3.10

ENV PYTHONUNBUFFERED 1
RUN pip install -U pip

RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/

RUN pip install -r requirements.txt

ADD . /code/

RUN python /code/manage.py migrate
RUN python /code/manage.py collectstatic --no-input
