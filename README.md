# Проект API_Yamdb

первй командный проект API были написаны модели и API к ним

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

git clone git@github.com:bogdanpracticum/api_yamdb.git

### Cоздать и активировать виртуальное окружение:

python -m venv env
source env/bin/activate

### Установить зависимости из файла requirements.txt:

python -m pip install --upgrade pip
pip install -r requirements.txt

### Выполнить миграции:

python manage.py makemigrations
python manage.py migrate 

### Запустить проект:

python manage.py runserver