ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}-buster
RUN pip install -U pip poetry
RUN poetry config virtualenvs.create false

# install python dependencies
WORKDIR /root
COPY pyproject.toml .
RUN poetry install

COPY . .
RUN poetry install
