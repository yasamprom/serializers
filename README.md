## Запуск в докере
```
git clone https://github.com/yasamprom/serializers.git
cd serializers
docker-compose up
```

## Запросы
Есть 4 формата данных, которые сейчас поддерживаются

В ответ на каждый запрос придет среднее время сериализации и десериализации

1) json 

    `curl -X GET  0.0.0.0:8080/test/1`
2) xml

    `curl -X GET  0.0.0.0:8080/test/2`
3) yaml

    `curl -X GET  0.0.0.0:8080/test/3`
4) message pack

    `curl -X GET  0.0.0.0:8080/test/4`