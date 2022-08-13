# Командный проект YaMDb
## _Описание_
Проект **YaMDb** собирает отзывы (**Review**) пользователей на произведения (**Titles**). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (**Category**) может быть расширен администратором.

Сами произведения в **YaMDb** не хранятся, здесь нельзя посмотреть фильм или послушать музыку. В каждой категории есть произведения: книги, фильмы или музыка.
Произведению может быть присвоен жанр (**Genre**) из списка предустановленных. Новые жанры может создавать только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (**Review**) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
### Пользовательские роли
- **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
- **Аутентифицированный пользователь (user)** — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
- **Модератор (moderator)** — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
- **Администратор (admin)** — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- **Суперюзер Django** должен всегда обладать правами администратора, пользователя с правами admin. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.

### Самостоятельная регистрация новых пользователей
- Пользователь отправляет **POST-запрос** с параметрами **email** и **username** на эндпоинт **/api/v1/auth/signup/**.        
- Сервис **YaMDB** отправляет письмо с кодом подтверждения (**confirmation_code**) на указанный адрес **email**.      
- Пользователь отправляет **POST-запрос** с параметрами **username** и **confirmation_code** на эндпоинт **/api/v1/auth/token/**,         
в ответе на запрос ему приходит token (**JWT-токен**).

### Ресурсы API YaMDb
- Ресурс ***auth***: аутентификация.
- Ресурс ***users***: пользователи.
- Ресурс ***titles***: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
- Ресурс ***categories***: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
- Ресурс ***genres***: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- Ресурс ***reviews***: отзывы на произведения. Отзыв привязан к определённому произведению.
- Ресурс ***comments***: комментарии к отзывам. Комментарий привязан к определённому отзыву.

## Технологии
- Python 3.7.9
- Django 2.2.16
- Django Rest Framework 3.12.4

## Установка и запуск проекта локально
1. **Клонируйте репозиторий:**
```sh
git clone https://github.com/DaneliyaPavel/infra_sp2.git
```

2. **Cоздать и активировать виртуальное окружение:**
```sh
python -m venv venv
source venv/Scripts/activate
```

3. **Обновить pip и установить зависимости из файла requirements.txt:**
```sh
python -m pip install --upgrade pip
pip install -r requirements.txt
```

4. **Выполнить миграции:**
```sh
cd yatube_api
python manage.py migrate
```

5. **Создать суперпользователя:**
```sh
python manage.py createsuperuser
```

6. **Проверка тестов:**
```sh
pytest
```

7. **Запустить проект:**
```sh
python manage.py runserver
```
Сервер запущен на странице:     
http://localhost:8000       
Спецификация и эндпоинты доступны в документации:       
http://localhost:8000/redoc/

## Запуск проекта в контейнерах

1. **В директории infra создайте файл ```.env``` с переменными окружения для работы с базой данных:**
```sh
# ...директория_проекта/infra/.env
# Укажите, что используете postgresql
DB_ENGINE=django.db.backends.postgresql
# Укажите имя созданной базы данных
DB_NAME=yatube
# Укажите имя пользователя
POSTGRES_USER=yatube_user
# Укажите пароль для пользователя
POSTGRES_PASSWORD=xxxyyyzzz
# Укажите localhost
DB_HOST=127.0.0.1
# Укажите порт для подключения к базе
DB_PORT=5432
```

2. **Измените файл settings.py, чтобы значения загружались из переменных окружения:**
```sh
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT')
    }
}
```

3. **Соберите контейнеры и запустите их:**
```sh
docker-compose up -d --build
```

4. **Выполните по очереди команды:**
```sh
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```

5. **Теперь проект доступен по адресу http://localhost/**


## Заполнить базу

1. Копируйте файл dump.json с локального компьютера на сервер.
Для такой задачи есть утилита scp (от англ. secure copy — «защищённая копия»). 
Она копирует файлы на сервер по протоколу SSH. Выполните команду:
```sh
# scp my_file username@host:<путь-на-сервере>

# Укажите IP своего сервера и путь до своей домашней директории на сервере
scp dump.json praktikum@84.201.161.196:/home/имя_пользователя/.../папка_проекта_с_manage.py/
```
2. После выполнения этой команды файл dump.json появится в директории проекта на вашем сервере.
Подключитесь к серверу и убедитесь в этом.

3. Работа на локальном компьютере завершена, продолжайте работать уже на сервере:
выполните команды для переноса данных с SQLite на PostgreSQL:
```sh
# Закинуть dump.json на сервер через scp и выполнить там

python3 manage.py shell  
# выполнить в открывшемся терминале:
>>> from django.contrib.contenttypes.models import ContentType
>>> ContentType.objects.all().delete()
>>> quit()

python manage.py loaddata dump.json
```


**Готово. Теперь все данные перенесены на сервер и доступны посетителям вашего проекта.
Откройте свой проект в браузере и убедитесь в этом.**

## Workflow

Main branch status

![main](https://github.com/DaneliyaPavel/yamdb_final/workflows/yamdb_final/badge.svg)

## Адрес развёрнутого проекта

Теперь проект доступен по адресу http://62.84.117.196/.

Зайдите на http://62.84.117.196/admin/ и убедитесь,
что страница отображается полностью: статика подгрузилась;

## Авторы

**_Павел Данелия_**

**_Александра Радионова_**

**_Александр Дёмин_**    

