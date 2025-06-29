**Веб-интерфейс для генерации контента через нейросети с акцентом на приватность и локальное хранение данных**

## Краткое описание

Проект предоставляет удобный веб-интерфейс для работы с генеративными нейросетями через чат-интерфейсы. **Все пользовательские данные (аудио, изображения, аккаунты) хранятся локально на вашей инфраструктуре.** Сложные задачи (распознавание речи, генерация изображений) выполняются через внешние API

#### Основные возможности

- **Аудио-чат:** Загрузите аудиофайл (русский язык) → получите распознанный текст
- **Изображения:** Опишите картинку текстом → получите сгенерированное изображение
- **Умный чат:** Общайтесь с AI-ассистентом (GPT-подобная модель)
- **Безопасность:** Данные хранятся **только на вашем ПК/сервере** (Minio, PostgreSQL)
- **Асинхронность:** Генерация контента в разных чатах одновременно (RabbitMQ)
- **Учетные записи:** Регистрация, авторизация, сессии (24 часа через Redis)

#### Технологический стек

| Категории                 | Технологии                                                                                     |
| ------------------------- | ---------------------------------------------------------------------------------------------- |
| Хранение                  | Minio (аудио/изображения), PostgreSQL (аккаунты, метаданные)                                   |
| Очереди                   | RabbitMQ (асинхронные задачи генерации)                                                        |
| Сессии/асинхронные задачи | Redis (сессии, task_id для асинхронных задач)                                                  |
| Фронтенд                  | React, Nginx (раздача статичных файлов)                                                        |
| Бэкенд                    | Python (микросервисы: gateway, аутентификация, нейросети)                                      |
| Мониторинг                | Promtail (сбор логов), Loki (хранение логов), Prometheus (сбор метрик), Grafana (визуализация) |
| Развёртывание             | Kubernetes (запуск всей инфраструктуры)                                                        |

#### Требования

1. **Docker Desktop (Kubernetes)**
2. **Доступ к внешним API (интернет)**
3. **Минимальные аппаратные ресурсы (около 1 ядра CPU и 1.5 Гб ОЗУ)**

#### Быстрый старт

1. **Клонируйте репозиторий**
```bash
git clone https://github.com/IvanovAnton4682671/BrainBox.git
cd BrainBox
```
2. **Настройте окружение**
```yaml
k8s/infra/2-neural/0-secret.yaml

apiVersion: v1
kind: Secret
metadata:
  name: brainbox-neural-secret
  namespace: brainbox
type: Opaque
stringData:
  MINIO_SECRET_KEY: "minioadmin"
  POSTGRES_URL: "postgresql+asyncpg://brainboxchatsadmin:brainboxchatsadmin@brainbox-postgresql-service.brainbox.svc.cluster.local:5432/brainboxchats"
  RABBITMQ_URL: "amqp://brainboxrabbitmq:brainboxrabbitmq@brainbox-rabbitmq-service.brainbox.svc.cluster.local:5672/"
  FOLDER_ID: "your-folder-id"
  OAUTH_TOKEN: "your-oauth-token"
```
3. **Соберите образы**
```bash
brainbox-authentication/
docker build -t brainbox-autentication:latest .

brainbox-client/
docker build -t brainbox-client:latest .

brainbox-gateway/
docker build -t brainbox-gateway:latest .

brainbox-neural/
docker build -t brainbox-neural:latest .
```
3. **Запустите систему**
   - Включите **Kubernetes** в **Docker Desktop**
   - Включите **отображение системных контейнеров**
```bash
k8s/scripts/
start.ps1
```
4. Откройте веб-интерфейс
   - Перейдите на http://localhost:30000/
4. Создайте аккаунт и начните использовать сервис
5. Смотрите мониторинг
   - Перейдите на http://localhost:31001/
   - Логин = **admin**, пароль = **admin**
   - Выберите **Dashboards**

#### Архитектура

![Проектирование](https://github.com/IvanovAnton4682671/BrainBox/blob/master/Проектирование.png)

#### Внеший вид сервиса

1. Веб-интерфейс
   ![Регистрация](https://github.com/IvanovAnton4682671/BrainBox/blob/master/Pasted%20image%2020250628235830.png)
   ![Авторизация](https://github.com/IvanovAnton4682671/BrainBox/blob/master/Pasted%20image%2020250628235851.png)
   ![Домашняя страница](https://github.com/IvanovAnton4682671/BrainBox/blob/master/Pasted%20image%2020250628235918.png)
   ![Речь в текст](https://github.com/IvanovAnton4682671/BrainBox/blob/master/Pasted%20image%2020250628235952.png)
   ![Генерация картинок](https://github.com/IvanovAnton4682671/BrainBox/blob/master/Pasted%20image%2020250629000010.png)
   ![Чат-бот](https://github.com/IvanovAnton4682671/BrainBox/blob/master/Pasted%20image%2020250629000145.png)
3. Мониторинг
   ![Логи](https://github.com/IvanovAnton4682671/BrainBox/blob/master/Pasted%20image%2020250629000529.png)
   ![Метрики](https://github.com/IvanovAnton4682671/BrainBox/blob/master/Pasted%20image%2020250629000553.png)
5. Развёрнутая инфраструктура
   ![k8s](https://github.com/IvanovAnton4682671/BrainBox/blob/master/Pasted%20image%2020250629000632.png)

#### Ключевые особенности

- **Локальность данных:** Аудио, изображения, метаданные чатов, учетные записи — **все хранится в вашей среде** (Minio, PostgreSQL)
- **Сессии 24/7:** Авторизуйтесь один раз — доступ на 24 часа через Redis
- **Неблокирующий UI:** Генерация изображения/текста в фоне (RabbitMQ, Dramatiq) → продолжайте общаться в других чатах
- **Готовый мониторинг:** Grafana + Prometheus + Loki + Promtail — для просмотра логов и метрик "из коробки"
- **Инфраструктура как код:** Полное управление через Kubernetes

#### Важно
- Проект **не включает** модели нейросетей, а только работает с ними через внешние API
- Конфигурация по умолчанию рассчитана **на локально использование**, однако при доработке может располагаться на хостинге

## Очень важно

- Разработка и тестирование велись **в системе Windows**, из-за этого пути в манифестах могут отличаться от стандартных в **Unix**
- В проекте используются YandexART API и YandexGPT API, чтобы получить токены и настроить работу с ними прочтите официальную документацию:
	- https://yandex.cloud/ru/docs/foundation-models/quickstart/yandexart
	- https://yandex.cloud/ru/docs/foundation-models/quickstart/yandexgpt
