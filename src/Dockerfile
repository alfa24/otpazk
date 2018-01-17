FROM python:3.6
#ENV PYTHONUNBUFFERED 1

#set time-zone
RUN echo "Asia/Irkutsk" > /etc/timezone && \
      dpkg-reconfigure -f noninteractive tzdata

RUN apt-get update &&  \
    apt-get install -y --no-install-recommends cron

# the django project
COPY ./otpazk /app/otpazk
COPY ./requirements /app/requirements
COPY ./manage.py /app/

# the local apps
COPY ./templates /app/templates

WORKDIR /app
RUN pip install  --default-timeout=100 -r /app/requirements/production.txt

#ENTRYPOINT ["/entrypoint.sh"]
CMD [ "./manage.py", "runserver", "0.0.0.0:8000" ]
