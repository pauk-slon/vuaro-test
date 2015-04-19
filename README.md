# vuaro-test — создание и управление заявками на кредит
Приложение предоставляет REST API для создания и управления заявками на кредит.

## Развёртывание
```sh
$ git clone https://github.com/pauk-slon/vuaro-test.git
$ cd vuaro-test
$ # Создание virtualenv (опционально)
$ virtualenv .venv
$ . .venv/bin/activate
$ # Если работаем с virtualenv, то, начиная с этого шага, считаем,
$ # что соответствующее виртуальное окружение активировано.
$ pip install -r requirements.txt
$ # Запускаем тесты, чтобы убедиться, что всё на своих местах
$ ./manage.py test loan_app.tests
$ # Запускаем миграции
$ ./manage.py migrate
$ # В текущей директории должен появиться файл БД, 
$ # убедимся в его присутствии
$ ls *.sqlite3
db.sqlite3
$ # Создаём суперпользователя Django
$ ./manage.py createsuperuser
$ # Вводим желаемые логин и пароль и удостоверяемся 
$ # в появлении надписи "Superuser created successfully".
$ # Запускаем HTTP-сервер
$ ./manage.py runserver
```

## Создание пользователей
1. Войти в [административную панель](http://127.0.0.1:8000/admin/), используя учётную запись суперпользователя Django.
2. В разделе [Пользователи и группы -› Пользователи](http://127.0.0.1:8000/admin/auth/user/) создать учётную запись пользователя и добавить её в одну из групп:
  - **loan_app_superuser** — суперпользователь приложения (не обязательно должен совпадать с суперпользователем Django);
  - **loan_app_bank_clerk** — работник банка;
  - **loan_app_user** — обычный пользователь.

## Web API
Путь к Web API: [/loan-app/rest/](http://127.0.0.1:8000/loan-app/rest/).
    
Ресурсы:

  - [users](http://127.0.0.1:8000/loan-app/rest/users/) — управление пользователями;
  - [field-types](http://127.0.0.1:8000/loan-app/rest/field-types/) — управления типами полей, которые могут быть использованы в заявлениях, в т. ч. *создание новых типов полей*;
  - [application-types](http://127.0.0.1:8000/loan-app/rest/application-types/) — управление типами заявлений: описывается тип завления, дочерним ресурсом [fields](http://127.0.0.1:8000/loan-app/rest/application-types/car-loan/fields/) определяется список полей, которые будет предложено заполнить при создании заявления данного типа;
  - [applications](http://127.0.0.1:8000/loan-app/rest/applications/) — управление заявлениями: в зависимости от привилегий данный ресурс предоставляет список доступных для пользователя заявлений и возможности по их созданию и модификации.

## Работа с заявками
### Получение access_token
1. [Зарегистрировать приложение](http://127.0.0.1:8000/admin/oauth2_provider/application/):
  - Client Type: confidential
  - Authorization Grant Type: Resource owner password-based
2. Выполнить:
```sh
$ curl -X POST -d "grant_type=password&username=<user_name>&password=<password>" -u"<client_id>:<client_secret>" http://localhost:8000/o/token/
```

### Создание заявки
```sh
$ curl -H "Authorization: Bearer <access_token>" -H "Content-Type: application/json" -X POST -d @create-application-test-request.json http://localhost:8000/loan-app/rest/applications/
```

### Получение списка заявок
```sh
$ curl -H "Authorization: Bearer <access_token>" http://localhost:8000/loan-app/rest/applications/
```
