#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python univote/manage.py collectstatic --no-input
python univote/manage.py migrate