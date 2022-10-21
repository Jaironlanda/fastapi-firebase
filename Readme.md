## Fastapi with Firebase Authentication

Firebase-admin and FastAPI project for authentication only.

#### Requirements

```bash
fastapi==0.84.0
pydantic==1.10.2
uvicorn==0.18.2
alembic==1.8.1
python-dotenv==0.19.2
sqlalchemy==1.4.35
asyncpg==0.26.0
pytz==2022.1
ua_parser==0.15.0
pytest
httpx
```

#### Docker Setup

```bash
docker compose up
```
#### Init Migrations

```bash
alembic init migrations
```

#### Autogenerate Migrations
```bash
alembic revision --autogenerate -m "init"
alembic upgrade head
```

#### Create DB
```bash
alembic upgrade head
```

#### Docker Exec

```bash
docker exec -w /myapp/app/v1 51fa0bf13ee3 alembic upgrade head
```