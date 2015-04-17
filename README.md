# vuaro_test

## Получение access_token
1. [Зарегистрировать приложение](http://127.0.0.1:8000/admin/oauth2_provider/application/):
  - Client Type: confidential
  - Authorization Grant Type: Resource owner password-based
    
2. Выполнить:
```sh
$ curl -X POST -d "grant_type=password&username=<user_name>&password=<password>" -u"<client_id>:<client_secret>" http://localhost:8000/o/token/
```

## Создание заявки
```sh
$ curl -H "Authorization: Bearer <access_token>" -H "Content-Type: application/json" -X POST -d @create-application-test-request.json http://localhost:8000/loan-app/rest/applications/
```

## Получение списка заявок
```sh
$ curl -H "Authorization: Bearer <access_token>" http://localhost:8000/loan-app/rest/applications/
```
