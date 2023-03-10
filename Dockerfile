FROM python:3.10

ENV PYTHONUNBUFFERED 1
RUN pip install -U pip

RUN mkdir /code
WORKDIR /code

# ADD requirements.txt /code/
ADD . /code/

RUN pip install -r requirements.txt

# RUN python /code/manage.py migrate
# RUN python /code/manage.py collectstatic --no-input

ENTRYPOINT ["sh", "/code/entrypoint.sh"]
