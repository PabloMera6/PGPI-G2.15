cd ./src
pip install -r requirements.txt
python ./manage.py migrate --run-syncdb
python ./manage.py loaddata populate.json
python ./manage.py runserver