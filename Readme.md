## Fastapi with Firebase Authentication

Firebase-admin and FastAPI project for authentication only.

Note: If you using docker please rename `temp.env` to `dev.env` in `environments/` directory, and enter a appropriate detail such as Firebase credential. 

### Firebase credentials is required ℹ️

More info about credentials: https://firebase.google.com/docs/admin/setup#initialize-sdk 

#### Please enter a valid credential in `environments/dev.env`

```bash
FIREBASE_TYPE=
FIREBASE_PROJECT_ID=
FIREBASE_PRIVATE_KEY_ID=
FIREBASE_PRIVATE_KEY=
FIREBASE_CLIENT_EMAIL=
FIREBASE_CLIENT_ID=
FIREBASE_AUTH_URI=
FIREBASE_TOKEN_URI=
FIREBASE_AUTH_PROVIDER_CERT_URL=
FIREBASE_CLIENT_CERT_URL=
```

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
firebase-admin
```

#### Docker Setup

```bash
docker compose build
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
docker exec -w /myapp/app/v1 <container id> alembic upgrade head
```