#!/bin/bash
set -e
cmd="$@"

# configure the crontab to check email
#CRONTAB_STR=(echo " */1 * * * * django /app/poll_helpdesk_email_queues.sh >> /tmp/foo.log 2>&1")
#crontab -l | grep -q $CRONTAB_STR  && echo 'entry exists' || (crontab -l 2>/dev/null; echo $CRONTB_STR) | crontab -

# the official postgres image uses 'postgres' as default user if not set explictly.
#if [ -z "$POSTGRES_USER" ]; then
#    export POSTGRES_USER=postgres
#fi

#function postgres_ready(){
#python << END
#import sys
#import psycopg2
#try:
#    conn = psycopg2.connect(dbname="$POSTGRES_DB", user="$POSTGRES_USER", password="$POSTGRES_PASSWORD", host="$POSTGRES_HOST")
#except psycopg2.OperationalError:
#    sys.exit(-1)
#sys.exit(0)
#END
#}

#until postgres_ready; do
#  >&2 echo "Postgres is unavailable - sleeping..."
#  sleep 1
#done

exec $cmd
