install dependecies with command
pip3 install -r requirements.txt

connect your PostreSQL database to Nice Cinema Application from settings.py
do not forget to create database "nice_cinema"
make migrations

python3 manage.py migrate

Run server

python3 manage.py runserver

for accepting admin panle simply go with url  http://runing_host/admin_dashboard
it required sign up. Create Admin account and add some movies and rooms

for book seats in Nice Cinema go with url http://runing_host/movies_list/
