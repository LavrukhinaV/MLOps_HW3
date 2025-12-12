# Домашнее задание 3. Создание воспроизводимого ML-pipeline с использованием DVC и MLflow 
**Автор:** *Лаврухина Виктория*

Этот проект демонстрирует развертывание ML-модели с помощью Canary Deployment и GitHub Actions.
---

## Структура репозитория
```
├── app/
│   ├── main.py
│   ├── model.pkl
│   └── requirements.txt
│
├── Dockerfile
├── docker-compose.blue.yml
├── docker-compose.green.yml
│
├── nginx/
│   └── nginx.conf
│
└── .github/
    └── workflows/
        └── deploy.yml
```