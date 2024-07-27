# Copyright (c) 2024 Robert Cronin
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:5000", "src.main:app"]