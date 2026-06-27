# Document Access Grant Service

## Setup

```bash
docker compose up -d
```

## Install

```bash
pip install -r requirements.txt
```

## Run Migrations

```bash
alembic upgrade head
```

## Run Server

```bash
uvicorn app.main:app --reload
```

## Run Tests

```bash
pytest
```
