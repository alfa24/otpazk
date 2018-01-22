#!/bin/bash
export PYTHONDONTWRITEBYTECODE='dontwrite'
ROOT=`dirname "${BASH_SOURCE[0]}"`
act="${ROOT}/.venv/bin/activate"

if [ ! -f "${act}" ]; then
    set -e
    virtualenv -p python3.6 .venv
    source ${act}
    pip install pip raven --upgrade
    pip install -r src/requirements/base.txt
    set +e
else
    source ${act}
fi


pip install -r src/requirements/base.txt
python src/manage.py migrate
python src/manage.py collectstatic --no-input
cp src/supervisor.conf /etc/supervisor/conf.d/supervisor.conf
update-rc.d supervisor enable
service supervisor start
service supervisor restart
supervisorctl reread
supervisorctl update
supervisorctl status



ARGS="$@"
if [ -n "${ARGS}" ]; then
    cd ${ROOT}
    exec $@
fi
