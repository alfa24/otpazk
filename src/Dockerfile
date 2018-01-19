FROM python:3.6
#ENV PYTHONUNBUFFERED 1

#set time-zone
RUN echo "Asia/Irkutsk" > /etc/timezone && \
      dpkg-reconfigure -f noninteractive tzdata

RUN apt-get update &&  \
    apt-get install -y --no-install-recommends cron supervisor

# the django project
COPY . /app/
COPY ./supervisor.conf /etc/supervisor/conf.d/supervisor.conf

WORKDIR /app
RUN pip install  --default-timeout=100 -r /app/requirements/production.txt

RUN chmod +x /app/entrypoint.sh
RUN chmod +x /app/tasks.sh

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["ping 127.0.0.1"]
