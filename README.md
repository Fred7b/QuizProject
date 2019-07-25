sudo -u postgres psql

Создадим базу данных;

CREATE DATABASE quizproject1;<br/>
CREATE USER quizproject1 WITH PASSWORD 'quizproject1'; --не нужен когда юзер создан<br/>
ALTER ROLE quizproject1 SET client_encoding TO 'utf8'; <br/>
ALTER ROLE quizproject1 SET default_transaction_isolation TO 'read committed'; <br/>
ALTER ROLE quizproject1 SET timezone TO 'UTC';<br/>
GRANT ALL PRIVILEGES ON DATABASE quizproject1 TO quizproject1;<br/>
\q<br/>
<br/><br/><br/
mkdir quizapp and cd<br/>
git clone this app<br/>
make venv: python3 -m venv venv_quizapp<br/>
source venv_quizapp/bin/activate<br/>
pip install -r requirements.txt<br/>
python manage.py createsuperuser<br/>
python manage.py makemigrations<br/>
python manage.py migrate<br/>
python manage.py runserver<br/>


![Image alt](/prtscr/start.png)
![Image alt](/prtscr/adminka.png)
![Image alt](/prtscr/registration.png)
![Image alt](/prtscr/profile.png)
![Image alt](/prtscr/profileedit.png)
![Image alt](/prtscr/completed_test_with_result.png)


