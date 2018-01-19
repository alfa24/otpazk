#!/bin/bash
set -e
cmd="$@"

echo " * * * * * root /app/task.sh" | crontab
/etc/init.d/cron restart
crontab -l

update-rc.d supervisor enable
service supervisor start
supervisorctl reread
supervisorctl update
supervisorctl status

exec $cmd
