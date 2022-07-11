FROM python:3.9-alpine


COPY ./docker/cron/cron_jobs /app/mycron
RUN mkdir "/logs"
RUN touch /logs/output.log
RUN touch /logs/err.log
RUN crontab /app/mycron

RUN mkdir -p /root/.aws/
COPY docker/minio/credentials /root/.aws/credentials

WORKDIR /app
COPY . /app
RUN pip install -r ./src/requirements.txt

CMD crond