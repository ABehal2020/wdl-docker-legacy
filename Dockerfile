FROM python:3
ENV PYTHONUNBUFFERED 1
COPY . /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt
