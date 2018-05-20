#!/bin/bash
source env/bin/activate
export all_proxy="http://proxy.cs.ui.ac.id:8080/"
pip3 install -r requirements.txt

python3 manage.py migrate --run-syncdb
python3 manage.py makemigrations
python3 manage.py migrate
nohup python3 manage.py runserver 152.118.25.3:8012