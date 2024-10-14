# Copyright (c) 2024 Robert Cronin
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

FROM bitnami/kubectl:latest as kubectl

FROM python:3.13-slim

COPY --from=kubectl /opt/bitnami/kubectl/bin/kubectl /usr/local/bin/kubectl

RUN apt-get update && apt-get install -y curl apt-transport-https gnupg2

RUN kubectl version --client

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:5000", "src.main:app"]