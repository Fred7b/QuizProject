sudo -u postgres psql

Создадим базу данных;

CREATE DATABASE quizproject1;
CREATE USER quizproject1 WITH PASSWORD 'quizproject1'; --не нужен когда юзер создан
ALTER ROLE quizproject1 SET client_encoding TO 'utf8'; 
ALTER ROLE quizproject1 SET default_transaction_isolation TO 'read committed'; 
ALTER ROLE quizproject1 SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE quizproject1 TO quizproject1;
\q

mkdir quizapp and cd
git clone this app
make venv: python3 -m venv venv_quizapp
source venv_quizapp/bin/activate
pip install -r requirements.txt
python manage.py createsuperuser
python manage.py makemigrations
python manage.py migrate
python manage.py runserver


![Image alt](/prtscr/start.png)
![Image alt](/prtscr/adminka.png)
![Image alt](/prtscr/registration.png)
![Image alt](/prtscr/profile.png)
![Image alt](/prtscr/profileedit.png)
![Image alt](/prtscr/completed_test_with_result.png)


