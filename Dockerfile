FROM python:3.8.10-slim

RUN apt-get update && apt-get install -y git gcc build-essential libssl-dev libffi-dev python-dev
RUN apt install -y pipenv

ARG SECRET_KEY
ENV SECRET_KEY ${SECRET_KEY}

COPY Pipfile /tmp
COPY Pipfile.lock /tmp
RUN cd /tmp && pipenv lock --keep-outdated --requirements > requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY . app/
WORKDIR app/

RUN python manage.py migrate

# They do not indicate which server to use, for practical purposes I use the server provided by django
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
ENTRYPOINT ["python"]
