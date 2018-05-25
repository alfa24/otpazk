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

update-rc.d supervisor enable
service supervisor stop
supervisorctl reread
supervisorctl update

pip install -r src/requirements/base.txt
cd src
python manage.py collectstatic --no-input
python manage.py migrate
cp supervisor.conf /etc/supervisor/conf.d/supervisor.conf

service supervisor start
supervisorctl status

ARGS="$@"
if [ -n "${ARGS}" ]; then
    cd ${ROOT}
    exec $@
fi

