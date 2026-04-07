FROM python:3.11-alpine

WORKDIR /app

# The cloud module requires pyyaml
RUN pip install --no-cache-dir pyyaml

COPY . /app/
