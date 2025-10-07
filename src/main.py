from fastapi import FastAPI
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from .core.api_register import regis_api_v1
from .database.core import get_db, Base
from .security.authorization import get_roles_permissions_map
from .security.cors import configure_middleware


# load the enviroments variable
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    db = next(get_db())
    try:
        get_roles_permissions_map(db)
    finally:
        db.close()

    yield  # The app runs while inside here

app = FastAPI(lifespan=lifespan)

configure_middleware(app)

# create entities in database or migrate database
# Base.metadata.create_all(bind=engine)

regis_api_v1(app)

