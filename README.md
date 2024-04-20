## Платформа для публикации платного контента
Реализовал платформу для публикации записей пользователями. Публикация может быть бесплатной, то есть доступной любому пользователю без регистрации, либо платной, которая доступна только авторизованным пользователям, которые оплатили разовую подписку.
Для реализации оплаты подписки я использовал Stripe. Регистрация пользователя доступна только по номеру телефона.

## Стэки:
1. python
2. postgresql
3. django
4. docker

## Для запуска проекта необходимо:

1. Клонируйте репозиторий
```bash
  git glone git@github.com:VladimirKovaliev/SPA_DRF_hw.git
```
2. Активируйте в нём виртуальное оружение, установите зависимости
```bash
  python source/bin/activate
```
```bash
  python -m pip install -r requirements.txt 
```
3. Создайте .env файл в корневой директории проекта и заполните следующие переменные:
```bash
SECRET_KEY=
TIME_ZONE=
DEBUG=

POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=

STRIPE_PUBLIC_KEY=
STRIPE_SECRET_KEY=
```

5. Выполните миграции
```bash
  python manage.py migrate
```
(если происходит ошибка, то пропишите 
'chmod u+rwx manage.py' и попробуйте выполнить миграции снова)


5. Запустите проект
```bash
    python manage.py runserver
```

## Для запуска докер контейнера:
```bash
  sudo docker compose build
```
```bash
  sudo docker compose up
```
