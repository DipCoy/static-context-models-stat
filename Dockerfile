FROM python:3.11
RUN pip install pipenv

COPY Pipfile Pipfile
RUN pipenv install --deploy