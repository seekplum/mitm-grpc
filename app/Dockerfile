FROM python:3.8-slim

WORKDIR /code

ADD ./requirements.txt /tmp/requirements.txt
RUN set -xe \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo "Asia/Shanghai" > /etc/timezone \
    && pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm -f /tmp/requirements.txt

COPY ./app ./app
COPY ./mygrpc ./mygrpc
ENV PYTHONPATH /code
RUN bash app/protos/gencode.sh

CMD ["/bin/bash", "-c", "uvicorn --workers 2 --host 0.0.0.0 --port 8084 app.main:app --reload"]
