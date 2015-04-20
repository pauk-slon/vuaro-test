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
Web API разработано на платформе Django REST framework. Поддерживаются HTTP Basic и OAuth 2.0 типы аутентификации. 
Также, для возможности использования обеспечивающего большую наглядность Browsable API, включена поддержка Session-аутентификации.

Для изучения ресурсов Web API [войдите](http://127.0.0.1:8000/api-auth/login/?next=/loan-app/rest/) в Browsable API, используя учётную запись, созданную в предыдущем пункте.

Ресурсы:

  - [users](http://127.0.0.1:8000/loan-app/rest/users/) — управление пользователями;
  - [field-types](http://127.0.0.1:8000/loan-app/rest/field-types/) — управления типами полей, которые могут быть использованы в заявлениях, в т. ч. *создание новых типов полей*;
  - [application-types](http://127.0.0.1:8000/loan-app/rest/application-types/) — управление типами заявлений: описывается тип завления, дочерним ресурсом [fields](http://127.0.0.1:8000/loan-app/rest/application-types/car-loan/fields/) определяется список полей, которые будет предложено заполнить при создании заявления данного типа;
  - [applications](http://127.0.0.1:8000/loan-app/rest/applications/) — управление заявлениями: в зависимости от привилегий данный ресурс предоставляет список доступных для пользователя заявлений и возможности по их созданию и модификации.


## Работа с заявками HTTP Basic Auth

### Создание заявки
```sh
$ curl -u <username>:<password> -H "Content-Type: application/json" -X POST -d @create-application-test-request.json http://localhost:8000/loan-app/rest/applications/
```

### Получение списка заявок
```sh
$ curl -u <username>:<password> http://localhost:8000/loan-app/rest/applications/
```


## Работа с заявками OAuth 2.0
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

## Работа с заявками через Browsable API

### Получение списка заявок

[Войдите](http://127.0.0.1:8000/api-auth/login/?next=/loan-app/rest/applications/) на страницу заявлений под вашей учётной записью.
На странице должен быть отображён список созданных заявлений, доступных вашей учётной записи (в зависимости от привилегий).

### Создание заявки

1. Откройте вкладку [Raw data](http://127.0.0.1:8000/loan-app/rest/applications/#post-generic-content-form)
2. Скопируйте содержимое файла `create-application-test-request.json` в форму и нажмите <kbd>POST</kbd>.

## Пример создания нового типа анкеты

Пройдём весь цикл создания нового типа анкеты, используя административную панель Django. 

(Те же самые действия можно выполнить и через Web API, делая соответствующие запросы к соответствующим ресурсам.)

### Создание нового типа поля

Создание нового типа поля возможно на основании базового типа данных и regex-шаблона, согласно которому будет происходить валидация значений данного типа.

Допустим нам нужно создать тип поля для хранения СНИЛСов. Реализуем его как строковый тип, состоящий из 11 цифр.

1. [Заявки на кредит -> Типы полей -> Добавить тип поля](http://127.0.0.1:8000/admin/loan_app/fieldtype/add/)
2. Значения полей:

  - Уникальный идентификатор: snils
  - Название: СНИЛС
  - Тип: CharValue
  - RegEx-шаблон: ^\d{11}$
3. <kbd>Сохранить</kbd>

### Создание нового типа анкеты
Создадим тип анкеты, состоящий из 4-х полей:

- фамилия;
- имя;
- отчество;
- СНИЛС.

#### Описание типа анкеты

1. [Заявки на кредит -> Типы акет -> Добавить тип анкеты](http://127.0.0.1:8000/admin/loan_app/applicationtype/add/)
2. Значения полей:

  - Уникальный идентификатор: test-loan
  - Название: Тестовый тип анкеты
  - Краткое название: ТЕСТ
3. <kbd>Сохранить</kbd>

#### Задание полей

1. Фамилия

  1. [Заявки на кредит -> Поля -> Добавить поле](http://127.0.0.1:8000/admin/loan_app/field/add/)
  2. Значения полей:

    - Application type: Тестовый тип заявки
    - Уникальный идентификатор: surname
    - Название: фамилия
    - Field type: строка
    - Обязательное для заполнения: да
  3. <kbd>Сохранить</kbd>
2. Имя

  1. [Заявки на кредит -> Поля -> Добавить поле](http://127.0.0.1:8000/admin/loan_app/field/add/)
  2. Значения полей:

    - Application type: Тестовый тип заявки
    - Уникальный идентификатор: given_name
    - Название: имя
    - Field type: строка
    - Обязательное для заполнения: да
  3. <kbd>Сохранить</kbd>

3. Отчество

  1. [Заявки на кредит -> Поля -> Добавить поле](http://127.0.0.1:8000/admin/loan_app/field/add/)
  2. Значения полей:

    - Application type: Тестовый тип заявки
    - Уникальный идентификатор: patronymic
    - Название: отчество
    - Field type: строка
    - Обязательное для заполнения: да
  3. <kbd>Сохранить</kbd>

4. СНИЛС

  1. [Заявки на кредит -> Поля -> Добавить поле](http://127.0.0.1:8000/admin/loan_app/field/add/)
  2. Значения полей:

    - Application type: Тестовый тип заявки
    - Уникальный идентификатор: snils
    - Название: СНИЛС
    - Field type: СНИЛС
    - Обязательное для заполнения: да
  3. <kbd>Сохранить</kbd>

### Создание анкеты

Таким образом был создан новый тип анкеты test-loan и можно приступать к созданию анкет на его основе.

JSON-запрос для создания анкеты типа test-loan будет следующим: 

```json
{
    "application_type": "test-loan",
    "values": [
        {
            "field": "surname",
            "value": "Сергеев"
        },
        {
            "field": "given_name",
            "value": "Владимир"
        },
        {
            "field": "patronymic",
            "value": "Игоревич"
        },
        {
            "field": "snils",
            "value": "12345678901"
        }
    ]
}
```
