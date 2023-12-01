cd ./src
pip install -r requirements.txt
python ./manage.py migrate --run-syncdb
python ./manage.py loaddata populate.json
coverage run manage.py test 
coverage report -m
python ./manage.py runserver