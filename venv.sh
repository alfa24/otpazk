#!/bin/bash
export PYTHONDONTWRITEBYTECODE='dontwrite'
ROOT=`dirname "${BASH_SOURCE[0]}"`
act="${ROOT}/.venv/bin/activate"

if [ ! -f "${act}" ]; then
    set -e
    virtualenv -p python3.6 .venv
    source ${act}
    pip install pip raven --upgrade
    pip install -r src/requirements/base.txt -r src/requirements/local.txt -r src/requirements/test.txt
    set +e
else
    source ${act}
fi

ARGS="$@"
if [ -n "${ARGS}" ]; then
    cd ${ROOT}
    exec $@
fi
