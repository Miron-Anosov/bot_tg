FROM python:3.11.4

COPY . /python_basic_diploma
WORKDIR /python_basic_diploma

RUN pip install pipenv
RUN pipenv install --ignore-pipfile



CMD ["pipenv", "run", "python", "main.py"]
