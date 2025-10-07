# FOOTPRINTS BACKEND

## Rerequirements
- environment variables
```
# DATABASE
DB_URL={Database connection url}

# JWT
SECRET_KEY={Secret key for jwt access token}
REFRESH_SECRET_KEY={Secret key for jwt refresh token}
ALGORITHM={encrypt algorithm}
ACCESS_TOKEN_EXPIRE_MINUTES={expire time by minutes for access token}
REFRESH_TOKEN_EXPIRE_DAYS={expire time by days for refresh token}
ISSUER={your issuer}

# S3
AWS_ACCESS_KEY_ID={aws-access-key-id}
AWS_SECRET_ACCESS_KEY={aws-secret-access-key}
AWS_REGION={aws-region}
AWS_S3_BUCKET={aws-bucket}
```

- Data migration
```bash
alembic ugrade head 
```

## Run service
```bash
# run with uvicorn
uvicorn src.main:app --host {host} --port {port}

# run with docker compose
sudo docker compose up --build
```