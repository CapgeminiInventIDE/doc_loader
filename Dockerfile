FROM python:3.6

ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get -y update && \
    apt-get -y install \
    poppler-utils \
    mupdf 

ADD requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -f requirements.txt

WORKDIR /opt/working