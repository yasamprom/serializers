## Запуск в докере
```
git clone https://github.com/yasamprom/serializers.git
cd serializers
docker-compose up
```

## Запросы
Есть 6 форматов данных, которые сейчас поддерживаются: xml, yaml, json, message pack, proto, avro

В ответ на каждый запрос придет среднее время сериализации и десериализации

Сейчас чтобы потестировать достаточно запустить ``docker-compose up``

Запустятся сразу все: клиент, прокси-сервер и главные сервисы. Дальше клиент отправит
10 случайных запросов и в логах будут ответы

## Docker
Для развертывания всех сервисов используется Dockerfile.common. Доугие докер файлы нужны для запуска сервисов по отдельности