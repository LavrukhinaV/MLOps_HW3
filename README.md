# Домашнее задание 3. Создание воспроизводимого ML-pipeline с использованием DVC и MLflow 
**Автор:** *Лаврухина Виктория*

Проект демонстрирует автоматизированное развертывание ML-модели с использованием Docker, Canary Deployment, GitHub Actions (CI/CD) и облачного деплоя в Render.

---

## Структура репозитория
```
.
├── app/
│   ├── main.py              # FastAPI ML-сервис
│   ├── model.pkl            # Обученная ML-модель
│   └── requirements.txt
│
├── nginx/
│   └── nginx.conf            # Балансировщик для Canary Deployment
│
├── docker-compose.blue.yml   # Стабильная версия сервиса (v1.0.0)
├── docker-compose.green.yml  # Canary-развертывание (v1.0.0 + v1.1.0)
├── Dockerfile
│
├── .github/workflows/
│   └── deploy.yml            # CI/CD pipeline
│
├── screenshots/              # Скриншоты проверки сервиса
│
└── README.md
```

---

### ML-сервис

Сервис реализован на **FastAPI** и использует заранее обученную модель (**model.pkl**).

Эндпоинты

1. `GET /health` — проверка доступности сервиса и версии модели

2. `POST /predict` — инференс модели

Версия модели передаётся через переменную окружения `MODEL_VERSION` и возвращается в ответах API.

Пример ответа `/health`:
```
{
  "status": "ok",
  "version": "v1.1.0"
}
```

---

### Контейнеризация и локальный запуск
Сборка Docker-образа
```
docker build -t ml-service:v1 .
```

Запуск стабильной версии (Blue)
```
docker compose -f docker-compose.blue.yml up -d
```

Проверка:
```
curl http://localhost:8080/health
```

---

### Стратегия развертывания: Canary Deployment

В проекте реализована стратегия **Canary Deployment**.

Компоненты:

* `ml_service_v1` — стабильная версия модели (v1.0.0);

* `ml_service_v2` — новая версия модели (v1.1.0);

* `nginx` — балансировщик трафика.

#### Распределение трафика (пример)
Начальный этап — 90% / 10%:
```
upstream ml_backend {
    server ml_service_v1:8080 weight=90;
    server ml_service_v2:8080 weight=10;
}
```

50% / 50%:
```
upstream ml_backend {
    server ml_service_v1:8080 weight=50;
    server ml_service_v2:8080 weight=50;
}
```
100% на новую версию:
```
upstream ml_backend {
    server ml_service_v2:8080;
}
```

**Rollback**
Откат выполняется изменением конфигурации Nginx:
```
upstream ml_backend {
    server ml_service_v1:8080;
}
```
и перезагрузкой балансировщика:
```
docker exec nginx_canary nginx -s reload
```

---

### CI/CD и деплой в облако
В репозитории настроен GitHub Actions workflow `.github/workflows/deploy.yml`, который:

* Проверяет корректность Docker-сборки;

* Триггерит реальный деплой сервиса в облако Render через HTTP API (Deploy Hook);

* Выполняет проверку доступности сервиса через `/health`.

Деплой запускается автоматически при пуше в ветку `main`.

---

### Облачный деплой (Render)
**Публичный URL сервиса:**
https://mlops-hw3.onrender.com/health
https://mlops-hw3.onrender.com/predict

**Использование GitHub Secrets при деплое**

Для обеспечения безопасности чувствительных данных и соответствия best practices, все параметры, необходимые для деплоя в облако, хранятся в GitHub Secrets и не включаются в код репозитория.

В CI/CD pipeline используются следующие секреты:
* `RENDER_DEPLOY_HOOK` - URL Deploy Hook в Render. Используется для запуска деплоя сервиса через HTTP API.

* `RRENDER_SERVICE_URL` - Публичный домен сервиса в Render. Используется для проверки эндпоинта `/health` после деплоя.

**Управление версией модели**

Версия модели (`MODEL_VERSION`) задаётся как переменная окружения на стороне Render, что позволяет:

* изменять версию модели без изменения кода и пересборки Docker-образа;

* централизованно управлять конфигурацией среды выполнения;

* отслеживать, какая версия модели развернута в текущем окружении через эндпоинт `/health`.

### Мониторинг и логирование
* Эндпоинт /health используется для мониторинга доступности сервиса и контроля версии модели;

* Версия модели (MODEL_VERSION) возвращается во всех ответах API;

* В приложении реализовано логирование:

  * старта сервиса;

  * запросов /health;

  * запросов /predict.

---

### Итог

В рамках задания реализовано:
* контейнеризованный ML-сервис;

* стратегия Canary Deployment с rollback;

* автоматизированный CI/CD pipeline;

* реальный деплой в облако через API;

* мониторинг и документация.
