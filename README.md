## Тестовое задание в одну большую AI компанию
# Cервис поиска по контактам на FastAPI
### Базовый функционал реализован по требованиям в task_description.txt

## Запуск

Нужен ```python:3.10``` (скорее всего работает и с версиями ниже, но гарантии нет)

Также каким-то образом должен быть запущен 
```sqlite 3.37.2``` (ситуация с версией та же что и с python)

### local run:
Установка зависимостей и запуск:
```shell
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8050
```
Если нет проблем - то в консоли будет что-то вида:
```shell
INFO:     Started server process [27148]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8050 (Press CTRL+C to quit)
```


### compose run:
1. build image:
```shell
docker build -t contacts-app .
```

2. run app:
 ```shell
docker compose up -d contacts_app
```
