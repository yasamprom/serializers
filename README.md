## Запуск в докере
```
git clone https://github.com/yasamprom/serializers.git
cd serializers
docker-compose up
```

## Запросы
Есть 7 форматов данных, которые сейчас поддерживаются: xml, yaml, json, message pack, proto, avro и native

В ответ на каждый запрос придет среднее время сериализации и десериализации

## Тестирование
1) ``docker-compose up``

2) ``echo "{'type': 'get_result', 'format': <format>}" | nc -u -w3 0.0.0.0 2000``

`<format>` принимает значения: 'xml', 'yaml', 'json', 'message pack', 'proto', 'avro' и 'native'

## Docker
Для развертывания всех сервисов используется Dockerfile.common. Другие докер файлы нужны для запуска сервисов по отдельности.
В текущем варианте каждый сервис запускается с использованием собранного образа, который
я предварительно опубликовал в [hub.docker.com](hub.docker.com)