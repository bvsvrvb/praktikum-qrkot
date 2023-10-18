# QRKot REST API

Учебный проект Яндекс Практикум (курс Python-разработчик плюс).

## Описание

**QRKot** - это приложение для Благотворительного фонда поддержки котиков.

#### Проекты

В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.
Пожертвования в проекты поступают по принципу *First In, First Out*: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.

#### Пожертвования

Каждый пользователь может сделать пожертвование и сопроводить его комментарием. Пожертвования не целевые: они вносятся в фонд, а не в конкретный проект. Каждое полученное пожертвование автоматически добавляется в первый открытый проект, который ещё не набрал нужную сумму. Если пожертвование больше нужной суммы или же в Фонде нет открытых проектов — оставшиеся деньги ждут открытия следующего проекта. При создании нового проекта все неинвестированные пожертвования автоматически вкладываются в новый проект.

#### Отчёт в Google Sheets

В приложении также реализована возможность формирования в гугл-таблице отчёта с закрытыми проектами, отсортированными по скорости сбора средств.

## Технологии

[![Python](https://img.shields.io/badge/Python-3.9-000000?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.78-000000?&logo=fastapi)](https://fastapi.tiangolo.com//)
[![SQLite](https://img.shields.io/badge/SQLite-3-000000?logo=sqlite)](https://www.sqlite.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4-000000)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/Alembic-1.7-000000)](https://alembic.sqlalchemy.org/)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-0.17-000000)](https://www.uvicorn.org/)

## Локальный запуск проекта

Клонировать репозиторий и перейти в директорию проекта:

```bash
git clone https://github.com/bvsvrvb/qrkot_spreadsheets.git
```

```bash
cd qrkot_spreadsheets
```

Создать `.env` файл с переменными окружения:

```
DATABASE_URL="sqlite+aiosqlite:///./fastapi.db"
SECRET="..."
FIRST_SUPERUSER_EMAIL="admin@example.com"
FIRST_SUPERUSER_PASSWORD="admin"
PASSWORD_MIN_LEN="3"
EMAIL="..."
TYPE="service_account"
PROJECT_ID="..."
PRIVATE_KEY_ID="..."
PRIVATE_KEY="..."
CLIENT_EMAIL="..."
CLIENT_ID="..."
AUTH_URI="https://accounts.google.com/o/oauth2/auth"
TOKEN_URI="https://oauth2.googleapis.com/token"
AUTH_PROVIDER_X509_CERT_URL="https://www.googleapis.com/oauth2/v1/certs"
CLIENT_X509_CERT_URL="..."
UNIVERSE_DOMAIN="googleapis.com"
```

Cоздать и активировать виртуальное окружение:

```bash
python -m venv venv
```

```bash
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```bash
python -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

Выполнить миграции:

```bash
alembic upgrade head
```

Запустить приложение:

```bash
uvicorn app.main:app --reload
```

## Автор

[Vlad Basarab](https://github.com/bvsvrvb)
